from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=59)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    due_date = models.DateField()

    def __str__(self):
        return self.title
