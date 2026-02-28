from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    )
    GENDER_CHOICES = (
            ("male", "Male"),
            ("female", "Female"),
        )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES , default='employee')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
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
    importance_degree = models.IntegerField(default=1)

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

    final_score = models.FloatField(null=True, blank=True)

    def calculate_final_score(self):
        from .services.scoring import ruleBase

        task = self.task
        user = task.assigned_to
        today = timezone.now().date()

        breach = Breach.objects.filter(
                user=user,
                date__month=today.month,
                date__year=today.year
            ).order_by("-date").first()

        breach_level = breach.level if breach else None

        attendance = Attendance.objects.filter(
                user=user,
                date=today
            ).first()
        arrival_time = attendance.arrival_time if attendance else None


        data = {
            "submissionTime": task.created_at,  # مؤقتًا
            "deadline": task.deadline,
            "taskNum": 1,
            "taskComplateAVR": self.objective_score or 0,
            "startWork": None,
            "endWork": None,
            "arrivalTime": arrival_time,
            "startMeeting": None,
            "endMeeting": None,
            "arrivalMeeting": None,
            "breachLevel": breach_level,
            "importanceDegree": task.importance_degree,
        }

        rule = ruleBase(data)
        return rule.resultScore()

        def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            self.final_score = self.calculate_final_score()
            super().save(update_fields=["final_score"])



        def __str__(self):
            return f"Evaluation for {self.task.title}"



class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    arrival_time = models.TimeField(null=True, blank=True)

class Breach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField()
    date = models.DateField()