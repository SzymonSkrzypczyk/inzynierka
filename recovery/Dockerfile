FROM golang:1.24.3-bookworm AS builder

WORKDIR /src
COPY db ./db
COPY recovery ./recovery
WORKDIR /src/recovery
RUN go mod download && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /recovery .

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /recovery ./recovery
ENTRYPOINT ["./recovery"]
