from rest_framework import generics
from .models import Task
from rest_framework import status
from .serializers import TaskSerializer
from django.utils.timezone import now
from rest_framework.response import Response

class TaskListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that handles listing and creating tasks.

    - Required: `title` (max 100 chars).  
    - Optional: `description` (max 500 chars), `due_date`, `photo`.  
    - If `photo` is uploaded, it's converted to grayscale and resized (max 800x800 px).  
    - Returns `201 Created` on success or `400 Bad Request` on validation errors.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to handle retrieving, updating, and deleting a single task.

    **Methods:**
    - **GET**: Retrieve task details by ID.
    - **PUT**: Fully or partially update a task.
    - **DELETE**: Remove the task permanently.

    **Behavior:**
    - Image processing (grayscale & resizing) is handled in the serializer.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class NearestDeadlineTaskView(generics.ListAPIView):
    """
    API endpoint to retrieve the task with the nearest upcoming due_date.

    - **GET**: Returns the task with the closest due_date (excluding null values).
    - **Response**: JSON with task details, or `404 Not Found` if no tasks have a due date.
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Filter tasks to get the one with the nearest due_date."""
        return Task.objects.filter(due_date__isnull=False, due_date__gte=now()).order_by("due_date")[:1]

    def list(self, request, *args, **kwargs):
        """Override list method to return 404 if no tasks are found."""
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No tasks with a due date found."}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)

    