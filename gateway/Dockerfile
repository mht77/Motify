FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/gateway
COPY /gateway/requirements.txt /code/gateway/
COPY /protos/account.proto /code/protos/
COPY /protos/artist.proto /code/protos/
COPY /gateway/run.sh /code/gateway/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ./run.sh
ADD *_pb2* /code/gateway/
COPY /gateway/ /code/gateway/
