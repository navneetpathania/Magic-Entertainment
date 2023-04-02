from django.db import models
from django.utils.timezone import now

class Museum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    Location = models.CharField(max_length=100, default="not available")
    subscription_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    url = models.URLField(max_length=300)

    def __str__(self):
        return self.name
