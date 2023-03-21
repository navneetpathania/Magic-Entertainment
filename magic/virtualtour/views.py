from django.shortcuts import render
from . models import Museum

def museum_list(request):
    museums = Museum.objects.all()
    return render(request,"virtualtour/virtualtour_list.html", {"museums":museums})
