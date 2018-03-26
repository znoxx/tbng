FROM alpine:latest

RUN apk add --update curl

COPY ./checkip /
ENTRYPOINT ["./checkip"]
