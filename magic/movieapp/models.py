from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    release_date = models.DateField()
    plot = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    poster = models.ImageField(upload_to='movie_posters/')
    video_file = models.FileField(upload_to='movies/')
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    subscription_only = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.title
