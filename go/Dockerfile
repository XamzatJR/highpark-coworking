FROM golang:1.12-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

WORKDIR /app

COPY . .

RUN go mod download

RUN go build -o main main.go routes.go utils.go

EXPOSE 4000

CMD ["./main"]