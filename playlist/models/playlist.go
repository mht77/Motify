package models

type Song struct {
	Id string `gorm:"primaryKey"`
}

type Playlist struct {
	Id          string `gorm:"primaryKey"`
	Name        string
	Songs       []Song `gorm:"many2many:playlist_songs;"`
	User        string
	DateCreated string
}
