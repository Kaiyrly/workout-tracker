from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    name = models.TextField(default='My workout')
    start_time = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    routine = models.ForeignKey('Routine', null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    performed = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Routine(models.Model):
    name = models.TextField()
    exercises = models.JSONField()

    def __str__(self):
        return self.name
