from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        # Setting up a dummy task for testing
        self.task = Task.objects.create(
            title="CI System Test",
            description="Testing GitHub Actions workflow"
        )

    def test_task_creation(self):
        # Verifying that the task was created correctly
        self.assertEqual(self.task.title, "CI System Test")
        self.assertTrue(isinstance(self.task, Task))