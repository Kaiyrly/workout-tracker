from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import HomeView, SignupView, ExerciseCreateView, WorkoutListView, workout_detail_view, ExerciseUpdateView, ExerciseDeleteView

app_name = "workoutnotes"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("create/", ExerciseCreateView.as_view(), name="create_exercise"),
    path("all/", WorkoutListView.as_view(), name="workout_list"),
    path("workouts/<int:workout_id>/", workout_detail_view),
    path("<int:pk>/update/", ExerciseUpdateView.as_view(), name="update_exercise"),
    path("<int:pk>/delete/", ExerciseDeleteView.as_view(), name="delete_exercise"),
]