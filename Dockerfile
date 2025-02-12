# Use an official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx  # Required for OpenCV

# Copy Pipenv files first to leverage Docker caching
COPY Pipfile Pipfile.lock ./

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --system

# Copy the entire project
COPY . .

# Expose port 8000 for the Django application
EXPOSE 8001

# Run Django migrations and start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
