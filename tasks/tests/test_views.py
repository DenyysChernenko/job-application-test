from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from datetime import timedelta
from django.utils import timezone
import os
import cv2
import numpy as np
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


TASK_PHOTOS_DIR = os.path.join(settings.MEDIA_ROOT, "task_photos")

def create_temp_image():
    """Helper function to create a temporary image for testing."""
    if not os.path.exists(TASK_PHOTOS_DIR):
        os.makedirs(TASK_PHOTOS_DIR)

    temp_path = os.path.join(TASK_PHOTOS_DIR, "test_image.jpg")

    image = np.ones((800, 800, 3), dtype="uint8") * 255
    cv2.imwrite(temp_path, image)

    with open(temp_path, "rb") as img_file:
        return SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/jpeg")


class TaskListCreateViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create sample tasks for testing (executed once for all tests)."""
        cls.task1 = Task.objects.create(title="Task 1", description="First test task", due_date="2025-06-01")
        cls.task2 = Task.objects.create(title="Task 2", description="Second test task", due_date="2025-07-01")
        cls.url = reverse("task-list")  

    def test_list_tasks(self):
        """Test retrieving a list of tasks."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        self.assertEqual(response.data[0]["title"], "Task 1")

    def test_create_task(self):
        """Test creating a new task with valid data."""
        data = {
            "title": "New Task",
            "description": "A new task description",
            "due_date": "2025-08-01"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)  
        self.assertEqual(Task.objects.last().title, "New Task")

    def test_create_task_invalid_data(self):
        """Test failing to create a task with invalid data (empty title)."""
        data = {"title": "", "description": "Invalid task", "due_date": "2025-08-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_long_title(self):
        """Test failing to create a task when the title exceeds 100 characters."""
        data = {"title": "A" * 101, "description": "Too long title", "due_date": "2025-08-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_long_description(self):
        """Test failing to create a task when the description exceeds 500 characters."""
        data = {"title": "Valid Title", "description": "A" * 501, "due_date": "2025-08-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_create_task_with_image(self):
        """Test creating a task with an image uploads and processes it correctly."""
        temp_image = create_temp_image()
        data = {
            "title": "Task with Image",
            "description": "Image test",
            "due_date": "2025-08-01",
            "photo": temp_image,
        }
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("photo", response.data)  

    def test_create_task_invalid_image(self):
        """Test uploading a non-image file should fail."""
        fake_file = SimpleUploadedFile("test.txt", b"Not an image", content_type="text/plain")
        data = {"title": "Bad Image", "description": "This should fail", "photo": fake_file}
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("photo", response.data)

    def test_create_task_future_due_date(self):
        """Test that a future due_date is valid."""
        data = {"title": "Future Task", "description": "Future due_date test", "due_date": "2030-01-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_create_task_past_due_date(self):
        """Test that a past due_date is allowed (if not restricted by model)."""
        data = {"title": "Past Task", "description": "Past due_date test", "due_date": "2020-01-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
    
    @classmethod
    def tearDownClass(cls):
        """Delete test images and clean up the task_photos folder after all tests."""
        super().tearDownClass()
        if os.path.exists(TASK_PHOTOS_DIR):
            for file in os.listdir(TASK_PHOTOS_DIR):
                file_path = os.path.join(TASK_PHOTOS_DIR, file)
                os.remove(file_path)
            os.rmdir(TASK_PHOTOS_DIR)  


class TaskDetailUpdateDeleteViewTestCase(APITestCase):
    """Test cases for retrieving, updating, and deleting tasks."""

    def setUp(self):
        """Create a sample task for testing."""
        self.task = Task.objects.create(
            title="Initial Task", description="Test description", due_date="2025-06-01"
        )
        self.url = reverse("task-detail", kwargs={"pk": self.task.id})  
        self.invalid_url = reverse("task-detail", kwargs={"pk": 9999})  

    def test_get_task_detail(self):
        """Test retrieving details of a single task, including photo if available."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Initial Task")
        self.assertEqual(response.data["description"], "Test description")
        self.assertIn("photo", response.data)  

    def test_get_non_existent_task(self):
        """Test retrieving a non-existent task should return 404."""
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task(self):
        """Test updating a task with valid data."""
        updated_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2025-07-01"
        }
        response = self.client.put(self.url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.description, "Updated description")

    def test_partial_update_task(self):
        """Test updating only part of the task using PATCH."""
        partial_update_data = {"title": "Partially Updated"}
        response = self.client.patch(self.url, partial_update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Partially Updated")
        self.assertEqual(self.task.description, "Test description")  

    def test_update_task_invalid_data(self):
        """Test failing to update a task with invalid data (empty title)."""
        invalid_data = {"title": "", "description": "Still testing", "due_date": "2025-07-01"}
        response = self.client.put(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_update_non_existent_task(self):
        """Test updating a non-existent task should return 404."""
        data = {"title": "Should Fail"}
        response = self.client.put(self.invalid_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_non_existent_task(self):
        """Test deleting a non-existent task should return 404."""
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_deleted_task(self):
        """Test retrieving a deleted task should return 404."""
        self.task.delete()  
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @classmethod
    def tearDownClass(cls):
        """Delete test images and clean up the task_photos folder after all tests."""
        super().tearDownClass()
        if os.path.exists(TASK_PHOTOS_DIR):
            for file in os.listdir(TASK_PHOTOS_DIR):
                file_path = os.path.join(TASK_PHOTOS_DIR, file)
                os.remove(file_path)
            os.rmdir(TASK_PHOTOS_DIR)


class NearestDeadlineTaskViewTestCase(APITestCase):
    def setUp(self):
        """Create sample tasks with different due dates."""
        self.task1 = Task.objects.create(title="Task 1", due_date=timezone.now() + timedelta(days=5))  
        self.task2 = Task.objects.create(title="Task 2", due_date=timezone.now() + timedelta(days=2))  
        self.task3 = Task.objects.create(title="Task 3", due_date=timezone.now() + timedelta(days=10)) 
        self.url = reverse("nearest-deadline")  

    def test_get_nearest_deadline_task(self):
        """Test retrieving the task with the closest due_date."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 2")  

    def test_no_tasks_with_due_date(self):
        """Test when there are no tasks with a due_date (should return 404)."""
        Task.objects.all().delete()  
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_multiple_tasks_with_due_dates(self):
        """Test when multiple tasks exist and only the nearest one is returned."""
        Task.objects.create(title="Extra Task", due_date=timezone.now() + timedelta(days=1))  
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Extra Task")

    def test_ignores_tasks_without_due_date(self):
        """Test that tasks without a due_date are ignored."""
        Task.objects.create(title="No Due Date Task", due_date=None)  
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]["title"], "No Due Date Task")  

    def test_ignores_past_due_dates(self):
        """Test that tasks with past due_dates are ignored."""
        Task.objects.create(title="Past Task", due_date=timezone.now() - timedelta(days=5))  
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]["title"], "Past Task")
