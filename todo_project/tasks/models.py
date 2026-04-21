from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('ZADANO', 'Zadáno'),
        ('ROZPRACOVANO', 'Rozpracováno'),
        ('DOKONCENO', 'Dokončeno'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Vysoká'),
        (2, 'Vyšší'),
        (3, 'Střední'),
        (4, 'Nižší'),
        (5, 'Nízká'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ZADANO')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title