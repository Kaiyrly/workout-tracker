from django.contrib import admin

from workoutnotes.models import Exercise, Workout, Routine

admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Routine)

