from tempfile import SpooledTemporaryFile

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_bytes

from music import settings


@deconstructible
class AzureStorageFile(File):
    def __init__(self, name, mode, storage, file):
        super().__init__(file, name)
        self.name = name
        self._mode = mode
        self._storage = storage
        self._is_dirty = False
        self._file = None
        self._path = name

    def _get_file(self):
        if self._file is not None:
            return self._file

        file = SpooledTemporaryFile(
            max_size=2*1024*1024,
            suffix=".AzureStorageFile",
        )

        if 'r' in self._mode or 'a' in self._mode:
            download_stream = self._storage.client(name=self.name).download_blob(self._path)
            download_stream.readinto(file)
        if 'r' in self._mode:
            file.seek(0)

        self._file = file
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def read(self, *args, **kwargs):
        if 'r' not in self._mode and 'a' not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return super().read(*args, **kwargs)

    def write(self, content):
        if ('w' not in self._mode and
                '+' not in self._mode and
                'a' not in self._mode):
            raise AttributeError("File was not opened in write mode.")
        self._is_dirty = True
        return super().write(content if isinstance(content, bytearray) else force_bytes(content))

    def close(self):
        if self._file is None:
            return
        if self._is_dirty:
            self._file.seek(0)
            self._storage._save(self.name, self._file)
            self._is_dirty = False
        self._file.close()
        self._file = None


# noinspection PyTypeChecker
class AzureStorage(Storage):

    def __init__(self):
        self.account_url = f"https://{settings.AZURE_STORAGE_NAME}.blob.core.windows.net/"
        self.default_credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(self.account_url,
                                                     credential=self.default_credential)

    def client(self, name):
        return self.blob_service_client.get_blob_client(container=settings.AZURE_STORAGE_CONTAINER,
                                                        blob=name)

    def _open(self, name, mode='rb'):
        return AzureStorageFile(name, mode, self)

    def _save(self, name, content):
        if isinstance(content, File):
            content = content.file

        content.seek(0)
        client = self.client(name)
        client.upload_blob(content)
        return name

    def path(self, name):
        cl = self.blob_service_client.get_container_client(container=settings.AZURE_STORAGE_CONTAINER)
        return cl.get_blob_client(name).url

    def delete(self, name):
        try:
            self.client(name).delete_blob(name)
        except ResourceNotFoundError:
            pass

    def exists(self, name):
        client = self.blob_service_client.get_blob_client(settings.AZURE_STORAGE_CONTAINER, blob=name)
        return client.exists()

    def listdir(self, path):
        pass

    def size(self, name):
        blob_client = self.client(name)
        properties = blob_client.get_blob_properties()
        return properties.size

    def url(self, name):
        return self.client(name).url

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def get_modified_time(self, name):
        pass
