from django.db import models


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    title = models.CharField(max_length=50, default="Unnamed")
    description = models.TextField(default="No description")
    status = models.CharField(max_length=20, default="pending", choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
