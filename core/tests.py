from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task, Evaluation

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        # 1. First, create a user because 'assigned_to' is mandatory
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            role="employee"
        )

        # 2. Now create the task with all required fields
        self.task = Task.objects.create(
            title="CI System Test",
            description="Testing GitHub Actions workflow",
            assigned_to=self.user,
            deadline=timezone.now() + timezone.timedelta(days=1)
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "CI System Test")
        self.assertEqual(self.task.assigned_to.username, "testuser")
        self.assertTrue(isinstance(self.task, Task))


class PerformancePlatformTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(
            username="mashael_dev",
            password="securepassword",
            role="employee"
        )

        
        self.task = Task.objects.create(
            title="Final Project CI",
            description="Testing full workflow",
            assigned_to=self.user,
            deadline=timezone.now() + timezone.timedelta(days=1)
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Final Project CI")
        self.assertTrue(isinstance(self.task, Task))

    def test_evaluation_link(self):
        
        evaluation = Evaluation.objects.create(
            task=self.task,
            evaluator=self.user,
            objective_score=95.0,
            subjective_score=90.0,
            feedback="Excellent progress in CI/CD implementation"
        )
        self.assertEqual(evaluation.task.title, "Final Project CI")
        self.assertEqual(self.task.evaluation.objective_score, 95.0)


class PerformancePermissionsTest(APITestCase):
    def setUp(self):
        # 1. Create a Manager
        self.manager = User.objects.create_user(
            username="manager_user",
            password="password123",
            role="manager"
        )
        
        # 2. Create an Employee
        self.employee = User.objects.create_user(
            username="employee_user",
            password="password123",
            role="employee"
        )

        # 3. Create a Task assigned to the employee
        self.task = Task.objects.create(
            title="Development Task",
            description="Fixing backend bugs",
            assigned_to=self.employee,
            deadline=timezone.now() + timezone.timedelta(days=1)
        )

    def test_employee_cannot_create_evaluation(self):
        # Log in as employee
        self.client.force_authenticate(user=self.employee)
        
        url = "/evaluations/"
        data = {
            "task": self.task.id,
            "objective_score": 90,
            "subjective_score": 85,
            "feedback": "Trying to evaluate myself"
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_create_evaluation(self):
        self.client.force_authenticate(user=self.manager)
        
        url = "/api/evaluations/"
        data = {
            "task": self.task.id,
            "objective_score": 95,
            "subjective_score": 90,
            "feedback": "Great work"
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)