# Generated by Django 5.2 on 2025-04-14 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0004_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='mot_de_passe',
            field=models.CharField(default='test123', max_length=128),
        ),
    ]
