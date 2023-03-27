from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Documentary(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    documentray_file = models.FileField(upload_to='documentries/')
    poster = models.ImageField(upload_to='documentrie_posters/')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    release_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscription_only = models.BooleanField(default=False)
    total_likes = models.IntegerField(validators=[MinValueValidator(0)])
    liked_by = models.ManyToManyField(User,blank=True)
    fav = models.ManyToManyField(User,null=True,blank=True, related_name='userfavdocumentray')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

class History(models.Model):
    documentary = models.ForeignKey(Documentary,on_delete=models.CASCADE, related_name='documentaryhistory')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userdocumentaryhistory')

    def __str__(self):
        return self.documentary.title