import os
import cv2
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework.test import APITestCase
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskSerializerTestCase(APITestCase):
    """Test cases for the TaskSerializer, including image processing."""

    def setUp(self):
        """Set up test data for tasks."""
        self.task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": None,
        }

    def create_temp_image(self):
        """Helper function to create a temporary white image without NumPy."""
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "test_image.jpg")

        # Create a blank white image (1000x1000 px) using OpenCV
        image = cv2.imread(temp_path)
        if image is None:
            image = cv2.cvtColor(cv2.UMat(255 * cv2.Mat.ones((1000, 1000, 3), dtype="uint8")).get(), cv2.COLOR_BGR2RGB)
            cv2.imwrite(temp_path, image)

        with open(temp_path, "rb") as img_file:
            return SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/jpeg")


    def test_valid_task_creation(self):
        """Test successful task creation."""
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, self.task_data["title"])

    def test_title_validation(self):
        """Test title validation (empty and too long)."""
        invalid_data = self.task_data.copy()
        invalid_data["title"] = ""
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("This field may not be blank.", serializer.errors["title"])

        invalid_data["title"] = "A" * 101
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Ensure this field has no more than 100 characters.", serializer.errors["title"])

    def test_description_validation(self):
        """Test description length validation."""
        invalid_data = self.task_data.copy()
        invalid_data["description"] = "A" * 501
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Ensure this field has no more than 500 characters.", serializer.errors["description"])

    def test_image_processing(self):
        """Test grayscale conversion and resizing of an uploaded image."""
        temp_image = self.create_temp_image()
        self.task_data["photo"] = temp_image

        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())

        task = serializer.save()
        image_path = os.path.join(settings.MEDIA_ROOT, task.photo.name)

        # Verify if the image exists after processing
        self.assertTrue(os.path.exists(image_path))

        # Load processed image and verify its properties
        processed_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(processed_img)

        # Check if it's converted to grayscale
        self.assertEqual(len(processed_img.shape), 2)

        # Check if it's resized correctly
        height, width = processed_img.shape
        self.assertLessEqual(height, 800)
        self.assertLessEqual(width, 800)

        # Cleanup test image
        os.remove(image_path)

    def test_task_update_with_new_image(self):
        """Test updating an existing task with a new image."""
        task = Task.objects.create(**self.task_data)
        temp_image = self.create_temp_image()

        update_data = {"photo": temp_image}
        serializer = TaskSerializer(task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_task = serializer.save()
        image_path = os.path.join(settings.MEDIA_ROOT, updated_task.photo.name)
        self.assertTrue(os.path.exists(image_path))

        # Cleanup test image
        os.remove(image_path)
