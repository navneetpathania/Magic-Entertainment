from django.contrib import admin
from .models import *
# register your models here.
admin.site.register(Director)
admin.site.register(Category)
admin.site.register(Documentary)
admin.site.register(History)