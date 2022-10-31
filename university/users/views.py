import os

from celery.result import AsyncResult
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, FileResponse

from users.models import User
from faculty.models import Direction, Group
from users.serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer
)
from faculty.serializers import DirectionSerializer, GroupSerializer
from common.permissions import UserPermission, AdminPermission, CuratorPermission
from university.tasks import create_statistic


class UserViewSet(
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Users view for create/update or get user"""
    queryset = User.objects.all()
    serializer_choises = {
        'create': CustomUserCreateSerializer,
        'retrieve': CustomUserSerializer,
        'partial_update': CustomUserCreateSerializer
    }
    permissions_choises = {
        'create': (AllowAny,),
        'retrieve': (CuratorPermission,),
        'partial_update': (CuratorPermission,),
        'me': (UserPermission,),
        'info': (AdminPermission,),
        'status': (AdminPermission,),
    }

    def get_serializer_class(self):
        return self.serializer_choises.get(self.action)

    def get_permissions(self):
        return tuple(
            permission() for permission in self.permissions_choises.get(
                self.action, (AdminPermission,)
            )
        )

    @action(
        detail=False,
        methods=('get',),
        url_path=r'me',
    )
    def me(self, request) -> Response:
        """get information of current user"""
        self.check_object_permissions(self.request, self.request.user)
        user = self.request.user
        serializer = CustomUserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=('get',),
        url_path=r'info',
    )
    def info(self, request) -> Response:
        """get statistic"""
        self.check_object_permissions(self.request, self.request.user)
        doc_name = self.request.data.get('doc_name', None)
        if not doc_name:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        directions = Direction.objects.select_related(
            'curator'
        ).prefetch_related('subjects').all()
        directions = DirectionSerializer(directions, many=True)
        groups = Group.objects.prefetch_related('students').all()
        groups = GroupSerializer(groups, many=True)

        task = create_statistic.delay(
            doc_name,
            directions.data,
            groups.data
        )

        print(os.getcwd())
        print(os.listdir(path=os.getcwd()))
        return Response(
            f'{task.task_id}',
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=('get',),
        url_path=r'status',
    )
    def status(self, *args, **kwargs) -> Response:
        """get status"""
        self.check_object_permissions(self.request, self.request.user)
        key = self.request.data['key']
        rid = AsyncResult(f'{key}')

        return Response(
            f'{rid.status}',
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=('get',),
        url_path=r'download',
    )
    def download(self, *args, **kwargs) -> Response:
        """get status"""
        self.check_object_permissions(self.request, self.request.user)
        key = self.request.data.get('key', None)
        if not key:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if os.path.exists(f'/app/data/{key}.xlsx'):
            with open(f'/app/data/{key}.xlsx', "rb") as file:
                response = FileResponse(
                    file.read(),
                    content_type='application/vnd' \
                                 '.openxmlformats-' \
                                 'officedocument.sp' \
                                 'readsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; ' \
                                                  'filename=/app' \
                                                  '/data/{key}.xlsx'
            return response

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
