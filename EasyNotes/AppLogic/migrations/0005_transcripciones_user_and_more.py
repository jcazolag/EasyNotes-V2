# Generated by Django 4.1.6 on 2023-04-27 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppLogic', '0004_alter_transcripciones_resumen'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcripciones',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fechasimportantes',
            name='transcripcion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppLogic.transcripciones'),
        ),
        migrations.AlterField(
            model_name='mygroups',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transcripciones',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppLogic.mygroups'),
        ),
    ]
