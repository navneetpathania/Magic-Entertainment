# Generated by Django 4.1.6 on 2023-02-08 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0004_genre_alter_movie_rating_movie_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='subscription_only',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='song',
            name='subscription_only',
            field=models.BooleanField(default=False),
        ),
    ]