package main

import (
	"fmt"
	"google.golang.org/grpc"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"net"
	"os"
	"playlist/models"
	"playlist/repositories"
	"playlist/services"
	proto "playlist/services/proto"
)

func main() {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d",
		os.Getenv("DB_HOST"), os.Getenv("DB_USER"), os.Getenv("DB_PASS"), os.Getenv("DB_NAME"), 5432)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	err = db.AutoMigrate(&models.Playlist{})
	if err != nil {
		panic("failed to migrate database")
	}
	val, ok := os.LookupEnv("GRPC_PORT")
	if !ok {
		val = "60051"
	}
	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", val))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	go StartListening(repositories.CreatePlaylistRepository(db))
	s := grpc.NewServer()
	service := services.CreatePlaylistService(repositories.CreatePlaylistRepository(db))
	proto.RegisterPlaylistServiceServer(s, service)
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
