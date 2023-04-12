FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/gateway
COPY /gateway/requirements.txt /code/gateway/
COPY /protos/account.proto /code/protos/
COPY /protos/artist.proto /code/protos/
COPY /protos/song.proto /code/protos/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY /gateway/ /code/gateway/
ENTRYPOINT ./run.sh