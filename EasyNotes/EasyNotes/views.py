from django.shortcuts import render
from AppLogic.models import *
from django.shortcuts import get_object_or_404

def home(request):
    if request.user.is_authenticated:
        if MyGroups.objects.filter(user_id=request.user.id):
            lastest_group = MyGroups.objects.filter(user_id=request.user.id).latest('creation_date')
            if Transcripciones.objects.filter(user_id=request.user.id):
                lastest_note = Transcripciones.objects.filter(user_id=request.user.id).latest('creation_date')
            else:
                lastest_note = None
            return render(request, 'home.html',{'note': lastest_note, 'group': lastest_group, 'op': True})
        else:
            return render(request, 'home.html', {'op': False})
    else:
        return render(request, 'home.html')