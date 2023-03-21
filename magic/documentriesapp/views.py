from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .models import Documentary, Category, History
from django.db.models import Count,Q
from collections import Counter

def documentary_list(request):
    documentaries = Documentary.objects.all()
    popular_documentaries = Documentary.objects.all().order_by('-total_likes')
    latest_documentaries = Documentary.objects.order_by('-created_at')
    categorys = Category.objects.annotate(num_documentary=Count('documentary')).filter(num_documentary__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_category = documentary_suggestion(request)
    recomendations = Documentary.objects.filter(Q(category__name__in=most_common_category)).exclude(documentaryhistory__user=request.user)[:10]
    return render(request, 'documentariesapp/documentary_list.html', {'documentaries': documentaries, 'popular_documentaries':popular_documentaries, 
    'latest_documentaries':latest_documentaries, 'categorys':categorys, 'recent_played':obj, 
    'recomendations':recomendations})

def documentary_suggestion(request):
    user = request.user
    history = user.userdocumentaryhistory.all()
    category =  [h.documentary.category for h in history]
    genre_counts = Counter(genre.name for genre in category)
    most_common_category = [genre_count[0] for genre_count in genre_counts.most_common(2)]
    return most_common_category

def documentary_download(request, pk):
    documentary = Documentary.objects.get(pk=pk)
    response = FileResponse(open(documentary.documentray_file.path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(documentary.documentray_file.name)
    return response

def play_documentary(request, pk):
    documentary = get_object_or_404(Documentary, pk=pk)
    return render(request, 'documentariesapp/documentary.html',{"documentary":documentary})

def historyView(request):
    if request.method == "POST":
        user = request.user
        documentary_id = request.POST['documentary_id']
        documentary = Documentary.objects.get(id=documentary_id)
        history, created = History.objects.get_or_create(user=user, documentary=documentary)
        if created:
            history.save()
            return redirect(f"/documentary/play_documentary/{documentary_id}")
        else:
            # If an object with the same documentary_id already exists, do nothing
            return redirect(f"/documentary/play_documentary/{documentary_id}")
    history = History.objects.filter(user=request.user)
    documentaries = []
    for i in history:
        documentaries.append(i.documentary)
    # documentaries = documentary.objects.filter(id__in=documentaries)
    return render(request,'documentaryapp/history.html', {"history":documentaries})