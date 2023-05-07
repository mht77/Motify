package services

import (
	"playlist/models"
	"playlist/services/proto"
	"testing"
)

type mockPlaylistRepo struct {
	playlists []models.Playlist
}

func createRepo() *mockPlaylistRepo {
	repo := mockPlaylistRepo{}
	repo.playlists = append(repo.playlists, models.Playlist{
		Id:          "1",
		Name:        "test",
		User:        "1",
		DateCreated: "Now",
	})
	return &repo
}

func (m *mockPlaylistRepo) Create(playlist models.Playlist) (*models.Playlist, error) {
	//TODO implement me
	panic("implement me")
}

func (m *mockPlaylistRepo) GetById(id string) (*models.Playlist, error) {
	for _, playlist := range m.playlists {
		if playlist.Id == id {
			return &playlist, nil
		}
	}
	return nil, nil
}

func (m *mockPlaylistRepo) GetAll(userId string) (*[]models.Playlist, error) {
	playlists := make([]models.Playlist, 0)
	for _, playlist := range m.playlists {
		if playlist.User == userId {
			playlists = append(playlists, playlist)
		}
	}
	return &playlists, nil
}

func (m *mockPlaylistRepo) Update(playlist models.Playlist) (*models.Playlist, error) {
	//TODO implement me
	panic("implement me")
}

func (m *mockPlaylistRepo) Delete(id string) error {
	//TODO implement me
	panic("implement me")
}

func TestGetAll(t *testing.T) {
	repo := createRepo()
	service := CreatePlaylistService(repo)

	all, err := service.GetAll(nil, &proto.UserId{
		Id: "1",
	})
	if err != nil {
		t.Error(err)
	}

	if len(all.Playlists) == 0 {
		t.Error("expected more than zero playlists")
	}

	all, err = service.GetAll(nil, &proto.UserId{
		Id: "2",
	})
	if len(all.Playlists) != 0 {
		t.Error("expected zero playlists")
	}
}

func TestGetById(t *testing.T) {
	repo := createRepo()
	service := CreatePlaylistService(repo)

	playlist, err := service.GetById(nil, &proto.SongId{
		Id: "1",
	})
	if err != nil {
		t.Error(err)
	}

	if playlist.Id != "1" {
		t.Error("expected id to be 1")
	}
}
