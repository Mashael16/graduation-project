from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES , default='employee')

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Task(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
        )
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class Evaluation(models.Model):
#     task = models.OneToOneField(Task, on_delete=models.CASCADE)
#     objective_score = models.IntegerField(default=0)
#     subjective_score = models.IntegerField(default=0)
#     feedback = models.TextField(blank=True)


# class Gamification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     xp = models.IntegerField(default=0)
#     badges = models.IntegerField(default=0)

class Evaluation(models.Model):

    task = models.OneToOneField(Task,
            on_delete=models.CASCADE,
            related_name="evaluation"
                            )

    evaluator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    # employee = models.ForeignKey(User, on_delete=models.CASCADE)
    objective_score = models.FloatField(null=True, blank=True)
    subjective_score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Evaluation for {self.task.title}"