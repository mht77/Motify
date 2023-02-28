from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

BASIC: Subscription
DESCRIPTOR: _descriptor.FileDescriptor
PREMIUM: Subscription
STANDARD: Subscription
UNKNOWN: Subscription

class Account(_message.Message):
    __slots__ = ["date_joined", "email", "id", "subscription", "username"]
    DATE_JOINED_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    date_joined: str
    email: str
    id: str
    subscription: Subscription
    username: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., username: _Optional[str] = ..., date_joined: _Optional[str] = ..., subscription: _Optional[_Union[Subscription, str]] = ...) -> None: ...

class GetAccountsRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAccountsResponse(_message.Message):
    __slots__ = ["accounts"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[Account]
    def __init__(self, accounts: _Optional[_Iterable[_Union[Account, _Mapping]]] = ...) -> None: ...

class Subscription(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
