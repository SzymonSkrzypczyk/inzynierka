FROM golang:1.24.3-bookworm AS builder

# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates

WORKDIR /app

COPY db/go.mod db/go.sum ./db/
RUN cd db && go mod download

COPY db ./db

RUN cd db && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o db_save .

FROM debian:bookworm-slim

# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/db/db_save ./db_save

# Default command
# Pass date at runtime, e.g. docker run ... 2025-01-05
ENTRYPOINT ["./db_save"]
