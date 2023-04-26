from django.shortcuts import render
import whisper as wp
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import *

import os

# Create your views here.

@login_required 
def groups(request):
    groups = MyGroups.objects.filter(user_id=request.user.id)
    return render(request, 'groups.html', {'groups': groups})

@login_required 
def newGroup(request):
    if request.method == 'GET':
        return render(request, 'newGroup.html')
    else:
        if request.method == 'POST':
            try:
                model = MyGroups(title=request.POST.get("title"),user_id=request.user.id)
                model.save()
                return redirect('groups')
            except Exception as e:
                return render(request, 'newGroup.html',{'error':e})

@login_required 
def Notes(request, group_id):
    transcripciones = Transcripciones.objects.filter(group_id=group_id)
    return render(request, 'notes.html', {'transcripciones': transcripciones, 'group_id': group_id})

@login_required 
def transcribe(request, group_id):
    show = False
    if request.method == 'GET':
        return render(request, 'transcribe.html',{'show': show})
    else:
        if request.method == 'POST' and request.FILES['audio_file']:
            show = True
            try:
                model = wp.load_model("base")
                audio = request.FILES["audio_file"]
                print(audio.size)
                fs = FileSystemStorage()
                filename = fs.save(audio.name, audio)
                name= audio.name
                result = model.transcribe("media/" + name, language="es", fp16 = False)
                if os.path.exists('media/' + name):
                    os.remove('media/' + name)
                return render(request,'transcribe.html', {'result': result, 'mensaje':'Este es el resultado de la transcripcion: ', 'show':show, "group_id": group_id})
            except Exception as e:
                return render(request, 'transcribe.html', {'error': e})
@login_required 
def newNote(request, group_id, result):
    if request.method == 'GET':
        return render(request, 'newNote.html', {"group_id": group_id, "result": result, "mensaje": 'Transcription: '})
    else:
        if request.method == 'POST':
            try:
                model = Transcripciones(title=request.POST.get("title"),transcripcion=result, group_id=group_id)
                model.save()
                return redirect('list', group_id=group_id)
            except Exception as e:
                return render(request, 'newNote.html',{'error':e})

@login_required 
def detail(request, transcripcion_id):
    transcripcion = get_object_or_404(Transcripciones,pk=transcripcion_id)
    return render(request, 'detail.html',{'transcripcion':transcripcion})






    