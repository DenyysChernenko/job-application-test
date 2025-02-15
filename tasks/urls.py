from django.urls import path
from .views import TaskListCreateView, TaskDetailUpdateDeleteView, NearestDeadlineTaskView

urlpatterns = [
    path("tasks", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailUpdateDeleteView.as_view(), name="task-detail"),
    path("tasks/nearest-deadline", NearestDeadlineTaskView.as_view(), name="nearest-deadline"),
]