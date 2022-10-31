from django.db import models


class Subject(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='name'
    )

    def __str__(self):
        return f'{self.name}'


class Group(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='name'
    )
    direction = models.ForeignKey(
        'faculty.Direction',
        on_delete=models.CASCADE,
        related_name='direction_groups',
        verbose_name='Direction'
    )
    students = models.ManyToManyField(
        'users.User',
        related_name='student_groups',
        verbose_name='Students',
        blank=True
    )

    def __str__(self):
        return f'{self.name}'


class Direction(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='name'
    )
    subjects = models.ManyToManyField(
        'faculty.Subject',
        related_name='directions',
        verbose_name='Subjects'
    )
    curator = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='directions',
        null=True,
        blank=True,
        verbose_name='Curator'
    )

    def __str__(self):
        return f'{self.name}'
