package services

import (
	"context"
	"fmt"
	"github.com/google/uuid"
	"log"
	"playlist/models"
	"time"
)

type PlaylistRepository interface {
	Create(playlist models.Playlist) (*models.Playlist, error)
	GetById(id string) (*models.Playlist, error)
	GetAll(userId string) (*[]models.Playlist, error)
	Update(playlist models.Playlist) (*models.Playlist, error)
	Delete(id string) error
}

type PlaylistService struct {
	PlaylistRepository PlaylistRepository
}

func CreatePlaylistService(playlistRepository PlaylistRepository) *PlaylistService {
	return &PlaylistService{PlaylistRepository: playlistRepository}
}

func (service *PlaylistService) Create(_ context.Context, request *CreateRequest) (*CreateResponse, error) {
	log.Printf("Received from user: %s, name: %s", request.User, request.Name)
	playlist := models.Playlist{}
	playlist.Name = request.Name
	playlist.User = request.User
	playlist.Id = uuid.NewString()
	now := time.Now()
	playlist.DateCreated = fmt.Sprintf("%d-%02d-%02d", now.Year(), now.Month(), now.Day())
	playlist.Songs = *SongModelsFromSongIds(request.Songs)
	created, err := service.PlaylistRepository.Create(playlist)
	if err != nil {
		return nil, err
	}
	return &CreateResponse{
		Id:          created.Id,
		User:        created.User,
		Name:        created.Name,
		DateCreated: created.DateCreated,
		Songs:       SongIdsFromSongModels(created.Songs),
	}, nil
}

func (service *PlaylistService) Delete(_ context.Context, request *SongId) (*SongId, error) {
	err := service.PlaylistRepository.Delete(request.Id)
	if err != nil {
		return nil, err
	}
	return &SongId{Id: request.Id}, nil
}

func (service *PlaylistService) GetById(_ context.Context, request *SongId) (*CreateResponse, error) {
	playlist, err := service.PlaylistRepository.GetById(request.Id)
	if err != nil {
		return nil, err
	}
	return &CreateResponse{
		Id:          playlist.Id,
		User:        playlist.User,
		Name:        playlist.Name,
		DateCreated: playlist.DateCreated,
		Songs:       SongIdsFromSongModels(playlist.Songs),
	}, nil
}

func (service *PlaylistService) GetAll(_ context.Context, request *UserId) (*GetAllResponse, error) {
	playlists, err := service.PlaylistRepository.GetAll(request.Id)
	if err != nil {
		return nil, err
	}
	playlistResponses := make([]*CreateResponse, 0)
	for _, playlist := range *playlists {
		playlistResponses = append(playlistResponses, &CreateResponse{
			Id:          playlist.Id,
			User:        playlist.User,
			Name:        playlist.Name,
			DateCreated: playlist.DateCreated,
			Songs:       SongIdsFromSongModels(playlist.Songs),
		})
	}
	return &GetAllResponse{Playlists: playlistResponses}, nil
}

func (*PlaylistService) mustEmbedUnimplementedPlaylistServiceServer() {
	panic("implement me")
}

type SongRepository interface {
	Create(song models.Song) (*models.Song, error)
	GetById(id string) (*models.Song, error)
}

func SongIdsFromSongModels(songs []models.Song) []string {
	songIds := make([]string, 0)
	for _, song := range songs {
		songIds = append(songIds, song.Id)
	}
	return songIds
}

func SongModelsFromSongIds(songs []string) *[]models.Song {
	songList := make([]models.Song, 0)
	for _, song := range songs {
		songList = append(songList, models.Song{Id: song})
	}
	return &songList
}
