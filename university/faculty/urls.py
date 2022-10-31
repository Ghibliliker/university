from django.urls import include, path
from rest_framework.routers import DefaultRouter

from faculty.views import SubjectViewSet, GroupViewSet, DirectionViewSet


router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'directions', DirectionViewSet, basename='directions')

urlpatterns = [
    path('', include(router.urls)),
]
