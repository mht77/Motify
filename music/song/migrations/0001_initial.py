# Generated by Django 4.1.7 on 2023-03-23 18:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artist', '0002_alter_artist_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=30)),
                ('NoPlays', models.PositiveBigIntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='song.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='artist.artist')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='song.genre')),
            ],
        ),
    ]