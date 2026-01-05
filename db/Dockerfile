FROM golang:1.24.3-bookworm AS builder

RUN apt-get update && apt-get install -y ca-certificates

WORKDIR /app/db

# Copy only Go module files first
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the db folder
COPY . ./

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o db_save .

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the binary
COPY --from=builder /app/db/db_save ./db_save

ENTRYPOINT ["./db_save"]
