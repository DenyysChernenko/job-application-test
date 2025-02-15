from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from datetime import timedelta

class TaskListCreateViewTestCase(APITestCase):
    def setUp(self):
        """Create sample tasks for testing."""
        self.task1 = Task.objects.create(title="Task 1", description="First test task", due_date="2025-06-01")
        self.task2 = Task.objects.create(title="Task 2", description="Second test task", due_date="2025-07-01")
        self.url = reverse("task-list")  

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
        data = {
            "title": "",  
            "description": "Invalid task",
            "due_date": "2025-08-01"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  


class TaskDetailUpdateDeleteViewTestCase(APITestCase):
    def setUp(self):
        """Create a sample task for testing."""
        self.task = Task.objects.create(title="Initial Task", description="Test description", due_date="2025-06-01")
        self.url = reverse("task-detail", kwargs={"pk": self.task.id})  

    def test_get_task_detail(self):
        """Test retrieving details of a single task."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Initial Task")
        self.assertEqual(response.data["description"], "Test description")

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

    def test_update_task_invalid_data(self):
        """Test failing to update a task with invalid data (empty title)."""
        invalid_data = {
            "title": "",  
            "description": "Still testing",
            "due_date": "2025-07-01"
        }
        response = self.client.put(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())  

    def test_get_deleted_task(self):
        """Test retrieving a deleted task (should return 404)."""
        self.task.delete()  
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NearestDeadlineTaskViewTestCase(APITestCase):
    def setUp(self):
        """Create sample tasks with different due dates."""
        self.task1 = Task.objects.create(title="Task 1", due_date=now() + timedelta(days=5))  
        self.task2 = Task.objects.create(title="Task 2", due_date=now() + timedelta(days=2))  
        self.task3 = Task.objects.create(title="Task 3", due_date=now() + timedelta(days=10)) 
        self.url = reverse("nearest-deadline")  

    def test_get_nearest_deadline_task(self):
        """Test retrieving the task with the closest due_date."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 2")  

    # def test_no_tasks_with_due_date(self):
    #     """Test when there are no tasks with a due_date (should return 404)."""
    #     Task.objects.all().delete()  
    #     response = self.client.get(self.url)

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_multiple_tasks_with_due_dates(self):
        """Test when multiple tasks exist and only the nearest one is returned."""
        Task.objects.create(title="Extra Task", due_date=now() + timedelta(days=1))  
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Extra Task")  
