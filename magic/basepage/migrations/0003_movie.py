# Generated by Django 4.1.6 on 2023-02-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0002_album_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_file', models.FileField(upload_to='movies/')),
                ('image', models.ImageField(upload_to='movies_pic/')),
                ('release_date', models.DateField()),
                ('director', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
            ],
        ),
    ]
