# Generated by Django 4.1.6 on 2023-04-25 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppLogic', '0003_alter_transcripciones_resumen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcripciones',
            name='resumen',
            field=models.TextField(blank=True, null=True),
        ),
    ]