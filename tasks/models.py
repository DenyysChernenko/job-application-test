from django.db import models

class Task(models.Model):
    """
    Model representing a Task.

    Attributes:
        title (str): The title of the task (required, max 100 characters).
        description (str, optional): A description of the task (optional, max 500 characters).
        due_date (date, optional): The optional deadline for the task.
        photo (ImageField, optional): An optional image associated with the task.
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=500)
    due_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="task_photos/", blank=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the Task model.
        
        Returns:
            str: The title of the task.
        """
        return self.title
