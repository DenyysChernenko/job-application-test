from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tasks.models import Task
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

class TaskAPITestCase(APITestCase):
    """
    API test case for Task endpoints.
    """

    def setUp(self):
        """
        Set up initial test data before each test.
        """
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            due_date=date.today(),
        )
        self.list_url = reverse("task-list")

    def test_create_task(self):
        """
        Test creating a new task via API.
        """
        data = {
            "title": "New Task",
            "description": "A new task created via API.",
            "due_date": date.today().isoformat(),
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_with_image(self):
        """
        Test creating a task with an image upload.
        """
        temp_image = self.create_temp_image()
        data = {
            "title": "Task with Image",
            "description": "This task has an image.",
            "due_date": date.today().isoformat(),
            "photo": temp_image,
        }
        self.client.post(self.list_url, data, format="multipart")
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertTrue(Task.objects.last().photo.name.startswith("task_photos/"))

    def test_get_task_list(self):
        """
        Test retrieving the list of tasks.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_task_detail(self):
        """
        Test retrieving a single task by ID.
        """
        url = reverse("task-detail", args=[self.task.id])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task(self):
        """
        Test updating a task.
        """
        url = reverse("task-detail", args=[self.task.id])
        data = {"title": "Updated Task"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self):
        """
        Test deleting a task.
        """
        url = reverse("task-detail", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def create_temp_image(self):
        """
        Creates a temporary image file for testing.
        """
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "test_image.jpg")

        # Create a simple blank image
        with open(temp_path, "wb") as img_file:
            img_file.write(b"\xFF" * 100) 

        with open(temp_path, "rb") as img_file:
            return SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/jpeg")
