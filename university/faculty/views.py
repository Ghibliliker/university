from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from faculty.models import Subject, Group, Direction
from faculty.serializers import (
    SubjectSerializer,
    GroupSerializer,
    GroupCreateUpdateSerializer,
    DirectionSerializer,
    DirectionCreateUpdateSerializer
)
from common.permissions import (
    AdminPermission, CuratorPermission, AdminOrReadOnly
)


class SubjectViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """subject view for create/update/del/get subjects"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (AdminPermission,)


class GroupViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """group view for create/update/get/del groups"""
    queryset = Group.objects.all()
    permissions_choises = {
        'create': (CuratorPermission,),
        'retrieve': (IsAuthenticated,),
        'partial_update': (CuratorPermission,),
        'list': (IsAuthenticated,),
        'destroy': (CuratorPermission,),
        'add_student': (CuratorPermission,),
    }
    serializer_choises = {
        'create': GroupCreateUpdateSerializer,
        'retrieve': GroupSerializer,
        'partial_update': GroupCreateUpdateSerializer,
        'list': GroupSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_choises.get(self.action)

    def get_permissions(self):
        return tuple(
            permission() for permission in self.permissions_choises.get(
                self.action, (AdminPermission,)
            )
        )

    @csrf_exempt
    @action(
        detail=True,
        methods=('patch',),
        url_path=r'add-student/(?P<user_id>\d+)'
    )
    def add_student(self, *args, **kwargs) -> Response:
        """add student to group"""
        self.check_object_permissions(self.request, self.request.user)
        group = self.get_object()
        student = get_object_or_404(User, pk=kwargs['user_id'])
        if group.students.count() < 20:
            group.students.add(student)
            group.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            'There are already 20 people in the group',
            status=status.HTTP_200_OK
        )


class DirectionViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """direction view for create/update/del/get directions"""
    queryset = Direction.objects.all()
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return DirectionSerializer
        return DirectionCreateUpdateSerializer
