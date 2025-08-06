import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Internship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="internships_created")

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.internship.title}"


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.internship.title}"


class TaskAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} -> {self.student.username}"


class TaskSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
    )
    task_assignment = models.OneToOneField(TaskAssignment, on_delete=models.CASCADE, related_name="submission")
    submitted_file = models.FileField(upload_to='task_submissions/', blank=True, null=True)
    submitted_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.task_assignment.student.username} for {self.task_assignment.task.title}"


class MockInterview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mock_interviews")
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="mock_interviews")
    scheduled_date = models.DateTimeField()
    interviewer_name = models.CharField(max_length=255)
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"


class ActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_logs")
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username