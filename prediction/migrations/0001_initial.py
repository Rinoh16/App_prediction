# Generated by Django 5.2 on 2025-04-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=10)),
                ('study_hours', models.FloatField()),
                ('previous_scores', models.FloatField()),
                ('attendance', models.FloatField()),
                ('predicted_score', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
