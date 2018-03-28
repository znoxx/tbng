FROM alpine:latest

RUN apk update && apk add --update curl

COPY ./checkip /
ENTRYPOINT ["./checkip"]
