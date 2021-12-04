#FROM python:3-alpine
FROM python:3.9
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
#RUN apk add build-base
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5001

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]