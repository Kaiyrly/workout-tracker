# Generated by Django 4.0.3 on 2022-03-24 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workoutnotes', '0004_alter_exercise_repsss'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workouts', to=settings.AUTH_USER_MODEL),
        ),
    ]
