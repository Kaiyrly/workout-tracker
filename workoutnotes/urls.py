from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import HomeView, SignupView, ExerciseCreateView, ExerciseListView, ExerciseDetailView, ExerciseUpdateView, ExerciseDeleteView

app_name = "workoutnotes"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("create/", ExerciseCreateView.as_view(), name="create_exercise"),
    path("all/", ExerciseListView.as_view(), name="exercises_list"),
    path("<int:pk>/", ExerciseDetailView.as_view(), name="exercise_detail"),
    path("<int:pk>/update/", ExerciseUpdateView.as_view(), name="update_exercise"),
    path("<int:pk>/delete/", ExerciseDeleteView.as_view(), name="delete_exercise"),
]