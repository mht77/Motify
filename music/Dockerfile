FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/gateway
COPY /music/requirements.txt /code/music/
COPY /protos/account.proto /code/protos/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY /music/ /code/music/
ENTRYPOINT ./run.sh