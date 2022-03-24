from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from  django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Exercise, Workout, Routine
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Sum

class SignupView(FormView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('workoutnotes:home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'workoutnotes/home.html'
    model = User
    context_object_name = 'user'

class WorkoutListView(LoginRequiredMixin, ListView):
    template_name = 'workoutnotes/workout_list.html'
    model = Workout
    context_object_name = 'workouts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workouts'] = Workout.objects.filter(user=self.request.user)
        return context



def workout_detail_view(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    exercises = Exercise.objects.filter(workout=workout)
    return render(
        request, 
        'workoutnotes/workout_detail.html', 
        {'workout': workout, 'exercises': exercises}
        )

def new_workout_view(request):
    new_workout = Workout()
    new_workout.user = request.user
    new_workout.save()
    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{new_workout.id}/')

def edit_workout_view(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    exercises = Exercise.objects.filter(workout=workout)
    routines = Routine.objects.all()
    return render(
        request, 
        'workoutnotes/edit_workout.html', 
        {'workout': workout, 'exercises': exercises, 'routines': routines}
        )

def start_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    workout.start_time = timezone.now()
    workout.save()
    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{workout_id}/')

def stop_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    workout.finish_time = timezone.now()
    workout.duration = workout.finish_time - workout.start_time
    workout.save()

    exercises = Exercise.objects.filter(workout=workout)
    i = 0
    for exercise in exercises:
        exercise.name = request.POST[f'name_{exercise.id}']
        exercise.weight = request.POST[f'weight_{exercise.id}']
        for s in exercise.repsss:
            exercise.repsss[s] = request.POST[f'rep_{s}']
            i += 1

        exercise.save()
    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{workout_id}/')

def save_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    workout.name = request.POST['name']
    workout.save()

    if workout.routine:
        routine = workout.routine
        routine = workout_to_routine(workout_id, routine)
        routine.save()

    return HttpResponseRedirect(f'/workoutnotes/workouts/{workout_id}/')

def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    workout.delete()
    return HttpResponseRedirect('/workoutnotes/all/')

def cancel_workout(request, workout_id):
    return delete_workout(request, workout_id)

def add_exercise_to_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    exercise = Exercise()

    exercise.workout = workout
    exercise.name = request.POST['name']
    exercise.weight = request.POST['weight']
    exercise.sets = request.POST['sets']
    reps = int(request.POST['reps'])
    exercise.repsss = dict()
    exercise.created_by = request.user
    
    cur_workout_exercises = Exercise.objects.filter(workout__id=workout_id)
    sets_num = cur_workout_exercises.aggregate(Sum('sets'))['sets__sum']
    sets_num = sets_num if sets_num else 0
    for i in range(sets_num, sets_num+int(exercise.sets)):
        exercise.repsss[i] = reps
    exercise.save()

    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{workout_id}/')
class AddExerciseView(CreateView):
    model = Exercise
    fields = ['name', 'weight', 'sets']
    template_name = 'workoutnotes/add_exercise.html'
    success_utl = reverse_lazy('workounotes:edi-workout')

    def form_valid(self, form):
        form.instance.workout = Workout.objects.get(id=self.kwargs['workout_id'])
        return super().form_valid(form)

def save_routine(request, workout_id):
    routine = Routine()
    routine.name = request.POST['name']
    workout = Workout.objects.get(id=workout_id)
    workout.routine = routine

    routine = workout_to_routine(workout_id, routine)

    routine.save()
    workout.save()

    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{workout_id}/')
    
def load_routine(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    routine_id = request.POST['selected_routine_id']
    routine = Routine.objects.get(id=routine_id)
    workout.routine = routine
    workout.save()


    for routine_exercise in routine.exercises:
        new_exercise = Exercise()
        new_exercise.workout = workout
        new_exercise.name = routine_exercise['name']
        new_exercise.weight = routine_exercise['weight']
        new_exercise.sets = routine_exercise['sets']
        new_exercise.repsss = routine_exercise['reps']
        new_exercise.created_by = request.user
        new_exercise.save()

    return HttpResponseRedirect(f'/workoutnotes/edit-workout/{workout_id}/')   
##################################################

def workout_to_routine(workout_id, routine):
    exercises = Exercise.objects.filter(workout__id=workout_id)
    routine_table = []
    
    for exercise in exercises:
        routine_table.append(
            {
                'name': exercise.name,
                'weight': exercise.weight,
                'sets': exercise.sets,
                'reps': exercise.repsss
            }
        )

    routine.exercises = routine_table

    return routine
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



