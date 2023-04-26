from django.db import models
from django.contrib.auth.models import User

class MyGroups(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

class Transcripciones(models.Model):
    title = models.CharField(max_length=100)
    transcripcion = models.TextField()
    resumen = models.TextField(null=True,blank=True)
    group = models.ForeignKey(MyGroups,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
 
class FechasImportantes(models.Model):
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    transcripcion = models.ForeignKey(Transcripciones,on_delete=models.CASCADE)
    

def __str__(self):
    return self.text