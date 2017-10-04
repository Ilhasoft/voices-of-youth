FROM mdillon/postgis:9.6-alpine

RUN apk update
RUN apk upgrade

COPY database.sh /docker-entrypoint-initdb.d

EXPOSE 5432
