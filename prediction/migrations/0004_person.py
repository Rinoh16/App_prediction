# Generated by Django 5.2 on 2025-04-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0003_remove_student_attendance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
            ],
        ),
    ]
