# Generated by Django 4.0.3 on 2022-03-24 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutnotes', '0002_routine_workout_exercise_workout'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='repsss',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
