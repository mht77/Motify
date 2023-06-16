package main

import (
	"fmt"
	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/vmihailenco/msgpack/v5"
	"log"
	"os"
	"playlist/models"
	"playlist/services"
	"time"
)

func StartListening(playlistRepo services.PlaylistRepository) {
	rabbit, ok := os.LookupEnv("RABBITMQ_HOST")
	if !ok {
		rabbit = "localhost"
	}
	conn, err := amqp.Dial("amqp://" + rabbit)
	if err != nil {
		panic(err)
	}

	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		panic(err)
	}
	defer ch.Close()

	err = ch.ExchangeDeclare("user-created",
		"fanout",
		true,
		false,
		false,
		false,
		nil)

	if err != nil {
		panic(err)
	}

	q, err := ch.QueueDeclare(
		"playlist_user_created",
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		panic(err)
	}

	err = ch.QueueBind(
		q.Name,
		"",
		"user-created",
		false,
		nil,
	)

	if err != nil {
		panic(err)
	}

	consume, err := ch.Consume(
		q.Name,
		"playlist_user_created",
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		panic(err)
	}

	var forever chan struct{}

	go func() {
		for d := range consume {
			var result map[string]interface{}
			log.Printf("Received a message: %s\n", d.Body)
			err := msgpack.Unmarshal(d.Body, &result)
			if err != nil {
				log.Fatalf("error: %s\n", err)
			} else {
				log.Printf("result: %s\n", result["id"])
				now := time.Now()
				playlist := models.Playlist{
					Name:        "Liked Songs",
					User:        result["id"].(string),
					Id:          uuid.NewString(),
					DateCreated: fmt.Sprintf("%d-%02d-%02d", now.Year(), now.Month(), now.Day()),
					Songs:       []models.Song{},
				}
				_, err = playlistRepo.Create(playlist)
				if err != nil {
					log.Fatalf("error: %s\n", err)
				}
			}
		}
	}()

	<-forever
}
