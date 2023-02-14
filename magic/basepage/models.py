from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    
    def __str__(self):
        return f'{self.name}'

class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_album.jpg', blank=True, null=True, upload_to='album_pic')
    release_date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name}'

class Song(models.Model):
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='songs/')
    subscription_only = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.title}'

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Movie(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='movies/')
    image = models.ImageField(upload_to='movies_pic/')
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    genres = models.ManyToManyField(Genre, related_name='movies')
    subscription_only = models.BooleanField(default=False)


    def __str__(self):
        return self.title


