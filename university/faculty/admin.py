from django.contrib import admin

from faculty.models import Subject, Group, Direction


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name'
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'direction'
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'curator'
    )
