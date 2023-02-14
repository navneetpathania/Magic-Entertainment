from django.contrib import admin
from .models import Artist, Album, Song, Movie, Genre

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Movie)
admin.site.register(Genre)
