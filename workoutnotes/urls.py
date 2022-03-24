from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import HomeView, SignupView, WorkoutListView, AddExerciseView, workout_detail_view, new_workout_view, edit_workout_view, start_workout, stop_workout, cancel_workout, save_workout, add_exercise_to_workout, save_routine, load_routine

app_name = "workoutnotes"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("new-workout/", new_workout_view),
    path("edit-workout/<int:workout_id>/", edit_workout_view),
    path("all/", WorkoutListView.as_view(), name="workout_list"),
    path("workouts/<int:workout_id>/", workout_detail_view),
    path("cancel-workout/<int:workout_id>/", cancel_workout),
    path("start-workout/<int:workout_id>/", start_workout),
    path("stop-workout/<int:workout_id>/", stop_workout),
    path("save-workout/<int:workout_id>/", save_workout),
    path("add-exercise/<int:workout_id>/", add_exercise_to_workout),
    path("save-routine/<int:workout_id>/", save_routine),
    path("load-routine/<int:workout_id>/", load_routine),
]