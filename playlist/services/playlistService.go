package services

import (
	"context"
	"fmt"
	"github.com/google/uuid"
	"log"
	"playlist/models"
	proto "playlist/services/proto"
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
	proto.UnimplementedPlaylistServiceServer
}

func CreatePlaylistService(playlistRepository PlaylistRepository) *PlaylistService {
	return &PlaylistService{PlaylistRepository: playlistRepository}
}

func (service *PlaylistService) Create(_ context.Context, request *proto.CreateRequest) (*proto.CreateResponse, error) {
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
	return &proto.CreateResponse{
		Id:          created.Id,
		User:        created.User,
		Name:        created.Name,
		DateCreated: created.DateCreated,
		Songs:       SongIdsFromSongModels(created.Songs),
	}, nil
}

func (service *PlaylistService) Delete(_ context.Context, request *proto.SongId) (*proto.SongId, error) {
	err := service.PlaylistRepository.Delete(request.Id)
	if err != nil {
		return nil, err
	}
	return &proto.SongId{Id: request.Id}, nil
}

func (service *PlaylistService) GetById(_ context.Context, request *proto.SongId) (*proto.CreateResponse, error) {
	playlist, err := service.PlaylistRepository.GetById(request.Id)
	if err != nil {
		return nil, err
	}
	return &proto.CreateResponse{
		Id:          playlist.Id,
		User:        playlist.User,
		Name:        playlist.Name,
		DateCreated: playlist.DateCreated,
		Songs:       SongIdsFromSongModels(playlist.Songs),
	}, nil
}

func (service *PlaylistService) GetAll(_ context.Context, request *proto.UserId) (*proto.GetAllResponse, error) {
	playlists, err := service.PlaylistRepository.GetAll(request.Id)
	if err != nil {
		return nil, err
	}
	playlistResponses := make([]*proto.CreateResponse, 0)
	for _, playlist := range *playlists {
		playlistResponses = append(playlistResponses, &proto.CreateResponse{
			Id:          playlist.Id,
			User:        playlist.User,
			Name:        playlist.Name,
			DateCreated: playlist.DateCreated,
			Songs:       SongIdsFromSongModels(playlist.Songs),
		})
	}
	return &proto.GetAllResponse{Playlists: playlistResponses}, nil
}

func (service *PlaylistService) AddSongsToPlaylist(_ context.Context, request *proto.AddRequest) (*proto.CreateResponse, error) {
	playlist, err := service.PlaylistRepository.GetById(request.Playlist)
	if err != nil {
		return nil, err
	}
	for _, songId := range request.Songs {
		exist := false
		for _, song := range playlist.Songs {
			if song.Id == songId {
				exist = true
				break
			}
		}
		if !exist {
			playlist.Songs = append(playlist.Songs, models.Song{Id: songId})
		}
	}
	updated, err := service.PlaylistRepository.Update(*playlist)
	if err != nil {
		return nil, err
	}
	return &proto.CreateResponse{
		Id:          updated.Id,
		User:        updated.User,
		Name:        updated.Name,
		DateCreated: updated.DateCreated,
		Songs:       SongIdsFromSongModels(updated.Songs),
	}, nil
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
