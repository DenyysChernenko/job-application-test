import cv2
import os
from rest_framework import serializers
from django.conf import settings
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles validation and image processing.
    """

    class Meta:
        model = Task  
        fields = "__all__" 

    def validate_title(self, value):
        """
        Ensures the title is not empty and does not exceed 100 characters.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 100:
            raise serializers.ValidationError("Title cannot exceed 100 characters.")
        return value

    def validate_description(self, value):
        """
        Ensures the description does not exceed 500 characters.
        """
        if value and len(value) > 500:
            raise serializers.ValidationError("Description cannot exceed 500 characters.")
        return value

    def process_image(self, task):
        """
        Processes the uploaded image:
        - Converts it to grayscale
        - Resizes it while maintaining aspect ratio (max size: 800x800)
        - Saves it back to the same location
        """
        if not task.photo:
            return  

        image_path = os.path.join(settings.MEDIA_ROOT, task.photo.name)
        img = cv2.imread(image_path)

        if img is None:
            return  
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        max_size = 800
        height, width = gray.shape
        scale = min(max_size / width, max_size / height)
        new_size = (int(width * scale), int(height * scale))
        resized = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)

        cv2.imwrite(image_path, resized)

    def create(self, validated_data):
        """
        Creates a new task and processes the uploaded image.
        """
        photo = validated_data.pop("photo", None)
        task = Task.objects.create(**validated_data)

        if photo:
            task.photo.save(photo.name, photo, save=False)
            self.process_image(task)

        return task

    def update(self, instance, validated_data):
        """
        Updates an existing task and reprocesses the image if updated.
        """
        photo = validated_data.get("photo", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if photo:
            self.process_image(instance)  

        return instance
