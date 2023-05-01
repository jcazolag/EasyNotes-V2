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
    elif request.method == 'POST':
        if not "audio_file" in request.FILES:   
            return render(request, 'transcribe.html', {'error': 'Selecciona un archivo de audio', 'show':show})
        else:
            audio = request.FILES["audio_file"]
            show = True
            try:
                
                print(audio.size)
                fs = FileSystemStorage()
                name = audio.name
                filename = fs.save(name, audio)
                result = whisper(name)

                if os.path.exists('media/' + name):
                    os.remove('media/' + name)
                
                return render(request,'transcribe.html', {'result': result, 'mensaje':'Este es el resultado de la transcripcion: ', 'show':show, "group_id": group_id})
            except Exception as e:
                print(e)
        

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
        if 'summary' in request.POST:
            if not transcripcion.resumen:
                input_text= f"Resume el siguiente texto: \"{transcripcion.transcripcion}\" "
                summary = chat(input_text)
                transcripcion.resumen=summary
                transcripcion.save()
                return render(request, 'detail.html',{'transcripcion':transcripcion, 'op':'summary'})
            else:
                return render(request, 'detail.html',{'transcripcion':transcripcion, 'op':'summary'})
        elif 'date' in request.POST:
            #print("date")
            dates = FechasImportantes.objects.filter(transcripcion_id=transcripcion_id)
            #print(dates)
            if dates:
                #print("date 1")
                dates = get_object_or_404(FechasImportantes,transcripcion_id=transcripcion_id)
                return render(request, 'detail.html',{'transcripcion':transcripcion, 'dates':dates, 'op':'dates'})
            else:
                #print("date 2")
                input_text= f"Del siguiente texto saca las fechas de examenes, tareas, actividades o eventos propuestos y dame una descripcion de dicho examen, tarea, actividad o evento: \"{transcripcion.transcripcion}\" \n\nEn caso de no haber, unicamente dime 'No se encontraron fechas' "
                result = chat(input_text)
                model = FechasImportantes(description=result,transcripcion_id = transcripcion_id,user_id=request.user.id, due_date=None)
                model.save()
                dates = get_object_or_404(FechasImportantes,transcripcion_id=transcripcion_id)
                return render(request, 'detail.html',{'transcripcion':transcripcion, 'dates':dates, 'op':'dates'})
        elif 'study_material' in request.POST:
            input_text= f"Dame o recomiendame material de estudio tales como libros, articulos o videos que esten relacionados con el tema de estudio del siguiente texto: \"{transcripcion.transcripcion}\" \nCon el siguiente formato:'El material de estudio recomendado es: - Libros: \n- Articulos: \n- Videos: ' \n\nSi no hay un tema de estudio respondeme con: 'No se puede sugerir material de estudio para este texto' \n\nsi hay varios temas de estudio, dame los materiales de estudio para cada tema de forma separada, pero con el mismo formato para cada tema. "
            result = chat(input_text)
            return render(request, 'detail.html',{'transcripcion':transcripcion, 'material':result, 'op':'study_material'})

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
            dates = FechasImportantes.objects.filter(transcripcion_id=transcripcion.id)
            if dates:
                date = dates[0]
            else:
                date=None
            return render(request, 'delete.html',{'object':transcripcion, 'dates':date, 'op': op})
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

def whisper(name):
    print("WHISPER")
    #audio_path = audio_file + name
    model = wp.load_model("small")
    # load audio and pad/trim it to fit 30 seconds
    audio = wp.load_audio('media/' + name)
    audio = wp.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = wp.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
    options = wp.DecodingOptions(fp16=False)
    result = wp.decode(model, mel, options)
    # print the recognized text
    return result