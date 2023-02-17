FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/gateway
COPY requirements.txt /code/gateway/
RUN pip install -r requirements.txt
COPY . /code/gateway/
