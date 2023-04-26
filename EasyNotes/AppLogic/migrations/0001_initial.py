# Generated by Django 4.1.6 on 2023-04-25 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transcripciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('transcripcion', models.TextField()),
                ('resumen', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppLogic.mygroups')),
            ],
        ),
        migrations.CreateModel(
            name='FechasImportantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('transcripcion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppLogic.transcripciones')),
            ],
        ),
    ]
