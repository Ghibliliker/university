from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        CURATOR = 'curator'
        STUDENT = 'student'
        ADMIN = 'admin'

    class Gender(models.TextChoices):
        FEMALE = 'female'
        MALE = 'male'

    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(
        max_length=7,
        choices=Roles.choices,
        default=Roles.STUDENT,
        verbose_name='Role'
    )
    gender = models.CharField(
        max_length=6,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name='Gender'
    )

    def __str__(self):
        return f'{self.email}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
