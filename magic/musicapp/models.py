from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    
    def __str__(self):
        return f'{self.name}'

class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_album.jpg', blank=True, null=True, upload_to='album_pic')
    release_date = models.DateField()
    artists = models.ManyToManyField(Artist)
    def __str__(self):
        return f'{self.name}'

class Song(models.Model):
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    album = models.ForeignKey(Album, null=True, on_delete=models.CASCADE, related_name='songs')
    artists = models.ManyToManyField(Artist)
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='songs/')
    subscription_only = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=now)
    def __str__(self):
        return f'{self.title}'



