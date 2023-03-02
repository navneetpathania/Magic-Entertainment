from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    checkouts_session_id = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} ({self.active})'




