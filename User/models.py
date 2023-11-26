from django.db import models
from django.contrib.auth.models import Permission
import uuid
from django.utils import timezone

class Account(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER_CHOICES = [
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    ]
    
    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'
    OTHER = 'OTHER'
    TYPE_CHOICES = [
        (STUDENT, 'STUDENT'),
        (TEACHER, 'TEACHER'),
        (OTHER, 'OTHER'),
    ]

    
    id = models.CharField(primary_key=True,default=uuid.uuid4, max_length=36)
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200) # service friends
    role = models.CharField(max_length=100,default='NORMAL')
    birthday = models.CharField(max_length=200)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    type = models.CharField(max_length=100,choices=TYPE_CHOICES)
    department = models.CharField(max_length=100, null=True, default=None)
    classroom = models.CharField(max_length=100, null=True, default=None)
    avt_url = models.URLField(default='https://i.pinimg.com/736x/c6/e5/65/c6e56503cfdd87da299f72dc416023d4.jpg')
    background_url = models.URLField(default='https://i.pinimg.com/736x/c6/e5/65/c6e56503cfdd87da299f72dc416023d4.jpg')
    createdAt = models.DateField(auto_now_add=True)
    updateAt = models.DateField(auto_now_add=True)

