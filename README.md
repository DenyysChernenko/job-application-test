# 🚀 Job Application Test

## 📝 Introduction

My name is **Denys Chernenko**, and this is my **Job Application Test** project.  
This repository contains a **Django-REST-based web application** that includes task management functionality and Leetcode-style coding challenges.

The project is fully **containerized with Docker**, making it easy to deploy, test, and run in any environment.

In this README, I'll guide you through:
- How to **run the application** using Docker
- How to **execute tests inside Docker**


## 🚀 Running the Application with Docker

This project is containerized using **Docker**, making it easy to run without setting up dependencies manually.

### **1️.1 Clone the Repository**
First, clone this repository from GitHub:
```sh
git clone https://github.com/DenyysChernenko/job-application-test.git
```

### **1.2 Navigate into the project directory**
```sh
cd job-application-test
```
### **1.3 Build the Docker image**

```sh
docker build -t job-application-test .
```

### **1.4 Run the Docker Container**
Once the image is built, start a container:
```sh
docker run -d -p 8002:8002 --name job-app-container job-application-test
```

### **1.5  Access the Application**
```sh
http://localhost:8002
```

## 🧪 How to Execute Tests Inside Docker

Once the application is running inside Docker, it can be executed with **unit tests** to verify that everything is working correctly.

---

### **2.1 Run All Tests**
To run all test cases inside the **Docker container**, use:
```sh
docker exec -it job-app-container python manage.py test
```