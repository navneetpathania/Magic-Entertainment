# Generated by Django 4.1.6 on 2023-02-05 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ImageField(blank=True, default='default_album.jpg', null=True, upload_to='album_pic'),
        ),
    ]