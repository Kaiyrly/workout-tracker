from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from  django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Exercise, Workout, Routine
from django.contrib.auth import login
from django.contrib.auth.models import User

class SignupView(FormView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('workoutnotes:home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class WorkoutListView(ListView):
    template_name = 'workoutnotes/workout_list.html'
    model = Workout
    context_object_name = 'workouts'

def workout_detail_view(request, workout_id):
    template_name = 'workout_detail.html'
    workout = Workout.objects.get(id=workout_id)
    exercises = Exercise.objects.filter(workout=workout)
    return render(
        request, 
        'workoutnotes/workout_detail.html', 
        {'workout': workout, 'exercises': exercises}
        )



class HomeView(TemplateView):
    template_name = 'workoutnotes/home.html'

##################################################
class ExerciseCreateView(CreateView):
    model = Exercise
    fields = ['name', 'sets', 'reps', 'weight']
    success_url = reverse_lazy('workoutnotes:home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = 'exercise'

class ExerciseUpdateView(UpdateView):
    model = Exercise
    fields = ['name', 'sets', 'reps', 'weight']
    context_object_name = 'exercise'

    def get_success_url(self) -> str:
        return reverse_lazy('workoutnotes:exercise_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.created_by

class ExerciseDeleteView(DeleteView):
    model = Exercise
    success_url = reverse_lazy('workoutnotes:exercises_list')

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.created_by



