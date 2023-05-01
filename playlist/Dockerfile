FROM golang:1.20

WORKDIR /app
COPY playlist/go.mod playlist/go.sum ./
#COPY ../protos/playlist.proto ../protos/playlist.proto
RUN go mod download
COPY playlist/ ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /playlist
EXPOSE 60051
CMD ["/playlist"]
