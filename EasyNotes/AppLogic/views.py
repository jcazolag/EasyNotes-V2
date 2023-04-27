from django.shortcuts import render
import openai
import whisper as wp
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
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
    group = get_object_or_404(MyGroups,pk=group_id)
    return render(request, 'notes.html', {'transcripciones': transcripciones, 'group': group})

@login_required 
def transcribe(request, group_id):
    show = False
    if request.method == 'GET':
        return render(request, 'transcribe.html',{'show': show})
    else:
        if request.method == 'POST' and request.FILES['audio_file']:
            show = True
            try:
                model = wp.load_model("small")
                audio = request.FILES["audio_file"]
                #print(audio.size)
                fs = FileSystemStorage()
                filename = fs.save(audio.name, audio)
                name= audio.name
                result = model.transcribe("media/" + name, language="es", fp16 = False, verbose=True)
                if os.path.exists('media/' + name):
                    os.remove('media/' + name)
                return render(request,'transcribe.html', {'result': result, 'mensaje':'Este es el resultado de la transcripcion: ', 'show':show, "group_id": group_id})
            except Exception as e:
                return render(request, 'transcribe.html', {'error': e})
@login_required 
def newNote(request, group_id, result):
    if request.method == 'GET':
        return render(request, 'newNote.html', {"result": result, "mensaje": 'Transcription: '})
    else:
        if request.method == 'POST':
            try:
                model = Transcripciones(title=request.POST.get("title"),transcripcion=result, group_id=group_id,user_id=request.user.id)
                model.save()
                return redirect('list', group_id=group_id)
            except Exception as e:
                return render(request, 'newNote.html',{'error':e})

@login_required 
def detail(request, transcripcion_id):
    if request.method =="GET":
        transcripcion = get_object_or_404(Transcripciones,pk=transcripcion_id)
        return render(request, 'detail.html',{'transcripcion':transcripcion, 'op': 'note'})
    else:
        transcripcion = get_object_or_404(Transcripciones,pk=transcripcion_id)
        if not transcripcion.resumen:
            input_text= f"Resume el siguiente texto: \"{transcripcion.transcripcion}\" "
            summary = chat(input_text)
            transcripcion.resumen=summary
            transcripcion.save()
            return render(request, 'detail.html',{'transcripcion':transcripcion, 'op':'summary'})
        else:
            return render(request, 'detail.html',{'transcripcion':transcripcion, 'op':'summary'})

@login_required 
def AdvOpt(request, object_id, op):
    if op =="groups":
         object = get_object_or_404(MyGroups,pk=object_id)
    elif op=="notes":
        object = get_object_or_404(Transcripciones,pk=object_id)

    return render(request, 'advancedOptions.html',{'object':object, 'op': op})

@login_required 
def delete(request, object_id, op):
    if request.method == "GET":
        if op =="groups":
            group = get_object_or_404(MyGroups,pk=object_id)
            transcripciones = Transcripciones.objects.filter(group_id=object_id)
            return render(request, 'delete.html',{'object':group, 'transcripciones': transcripciones, 'op': op})
        elif op == "notes":
            transcripcion = get_object_or_404(Transcripciones,pk=object_id)
            dates = FechasImportantes.objects.filter(transcripcion_id=object_id)
            return render(request, 'delete.html',{'object':transcripcion, 'dates':dates, 'op': op})
    else:
        if op =="groups":
            group = get_object_or_404(MyGroups,pk=object_id)
            group.delete()
            return redirect('groups')
        elif op == "notes":
            transcripcion = get_object_or_404(Transcripciones,pk=object_id)
            group = transcripcion.group_id
            transcripcion.delete()
            return redirect('list', group_id=group)

@login_required 
def update(request, object_id, op):
    if request.method == "GET":
        if op =="groups":
            group = get_object_or_404(MyGroups,pk=object_id)
            return render(request, 'update.html',{'object':group, 'op': op})
        elif op == "notes":
            transcripcion = get_object_or_404(Transcripciones,pk=object_id)
            return render(request, 'update.html',{'object':transcripcion, 'op': op})
    else:
        if op =="groups":
            group = get_object_or_404(MyGroups,pk=object_id)
            title = request.POST["title"]
            group.title= title
            group.save()
            return redirect('groups')
        elif op == "notes":
            transcripcion = get_object_or_404(Transcripciones,pk=object_id)
            title = request.POST["title"]
            note = request.POST["note"]
            transcripcion.title= title
            transcripcion.transcripcion= note
            transcripcion.save()
            print("working progress")
            return redirect('list', group_id=transcripcion.group_id)
        
def chat(text):
    input_text = text
    #print("este es el input text: " + input_text)
    openai.api_key = "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"
    completions = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-0301",
    messages=[{"role": "user", "content": input_text}])
    output_text = completions.choices[0].message.content
    return output_text