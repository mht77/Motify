package repositories

import (
	"gorm.io/gorm"
	"playlist/models"
)

type PlaylistRepository struct {
	db *gorm.DB
}

func CreatePlaylistRepository(db *gorm.DB) *PlaylistRepository {
	return &PlaylistRepository{db: db}
}

func (repository *PlaylistRepository) Create(playlist models.Playlist) (*models.Playlist, error) {
	err := repository.db.Create(&playlist).Error
	return &playlist, err
}

func (repository *PlaylistRepository) GetById(id string) (*models.Playlist, error) {
	var playlist models.Playlist
	err := repository.db.Preload("Songs").Where("id = ?", id).First(&playlist).Error
	return &playlist, err
}

func (repository *PlaylistRepository) GetAll(userId string) (*[]models.Playlist, error) {
	var playlists []models.Playlist
	err := repository.db.Preload("Songs").Find(&playlists, `"user" = ?`, userId).Error
	return &playlists, err
}

func (repository *PlaylistRepository) Update(playlist models.Playlist) (*models.Playlist, error) {
	err := repository.db.Save(&playlist).Error
	return &playlist, err
}

func (repository *PlaylistRepository) Delete(id string) error {
	playlist, err := repository.GetById(id)
	if err != nil {
		return err
	}
	err = repository.db.Model(&playlist).Association("Songs").Clear()
	if err != nil {
		return err
	}
	err = repository.db.Where("id = ?", id).Delete(&models.Playlist{}).Error
	return err
}
