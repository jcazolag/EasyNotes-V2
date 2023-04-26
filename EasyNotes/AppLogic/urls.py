from django.urls import path
from . import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('notes/<int:group_id>', views.Notes, name='list'),
    path('note/<int:transcripcion_id>', views.detail, name='detail'),
    path('<int:group_id>', views.transcribe, name='transcribe'),
    path('newGroup', views.newGroup, name='newGroup'),
    path('newNote/<int:group_id>/<str:result>', views.newNote, name='newNote'),
]