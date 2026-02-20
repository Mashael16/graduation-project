from django.test import TestCase
from django.utils import timezone
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