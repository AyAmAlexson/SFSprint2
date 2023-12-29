from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .managers import MountainPassManager, UserManager
from .serializers import MountainPassSerializer
from .models import *
import json
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SubmitDataView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'other_titles': openapi.Schema(type=openapi.TYPE_STRING),
                'connect': openapi.Schema(type=openapi.TYPE_STRING),
                'add_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                'coords': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                        'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                        'height': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['latitude', 'longitude', 'height'],
                ),
                'level': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winter': openapi.Schema(type=openapi.TYPE_STRING),
                        'summer': openapi.Schema(type=openapi.TYPE_STRING),
                        'autumn': openapi.Schema(type=openapi.TYPE_STRING),
                        'spring': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['summer', 'autumn'],
                ),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'data': openapi.Schema(type=openapi.TYPE_STRING),
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                        required=['data', 'title'],
                    ),
                ),
            },
            required=['beauty_title', 'title', 'add_time', 'user', 'coords', 'level', 'images'],
        ),
        responses={200: "OK - Success", 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user')

            if not user_id:
                return Response({'status': 400, 'message': 'Bad User ID', 'id': None}, status=status.HTTP_400_BAD_REQUEST)

            result = MountainPassManager.submit_data(data, user_id)
            return Response(result, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({'status': 400, 'message': "Can't read the data", 'id': None}, status=status.HTTP_400_BAD_REQUEST)

class AddNewUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'fam': openapi.Schema(type=openapi.TYPE_STRING),
                'otc': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'phone', 'name', 'fam', 'otc'],
        ),
        responses={200: "OK - Success", 400: "Bad Request"},
    )
    def post(self, request, *arg, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            result = UserManager.submit_data(data)
            return Response(result, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({'status': 400, 'message': 'Input Data Error', 'id': None}, status=status.HTTP_400_BAD_REQUEST)


class GetMountainPassView(APIView):
    def get(self, request, pk, *args, **kwargs):
        mountain_pass = get_object_or_404(MountainPass, pk=pk)
        context = {'request': request}
        serializer = MountainPassSerializer(mountain_pass, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditMountainPassView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='ID of the mountain pass to edit'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'other_titles': openapi.Schema(type=openapi.TYPE_STRING),
                'connect': openapi.Schema(type=openapi.TYPE_STRING),
                'coords': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                        'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                        'height': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['latitude', 'longitude', 'height'],
                ),
                'level': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winter': openapi.Schema(type=openapi.TYPE_STRING),
                        'summer': openapi.Schema(type=openapi.TYPE_STRING),
                        'autumn': openapi.Schema(type=openapi.TYPE_STRING),
                        'spring': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['summer', 'autumn'],
                ),
            },
        ),
        responses={
            200: "OK - Success",
            400: "Bad Request",
            404: "Not Found",
        },
        exclude=['id'],  # Exclude the 'id' parameter
    )
    def patch(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            mountain_pass = get_object_or_404(MountainPass, pk=pk)

            if not mountain_pass:
                return Response({'status': 400, 'message': 'Mountain Pass Not Found', 'id': None}, status=status.HTTP_400_BAD_REQUEST)

            if mountain_pass.status != 'new':
                return Response({'status': 0, 'message': 'Нельзя редактировать запись в статусе, отличном от "new".'}, status=status.HTTP_400_BAD_REQUEST)

            mountain_pass.beauty_title = data['beauty_title'] if 'beauty_title' in data else mountain_pass.beauty_title
            mountain_pass.title = data['title'] if 'title' in data else mountain_pass.title
            mountain_pass.other_titles = data['other_titles'] if 'other_titles' in data else mountain_pass.other_titles
            mountain_pass.connect = data['connect'] if 'connect' in data else mountain_pass.connect
            mountain_pass.coord = data['coord'] if 'coord' in data else mountain_pass.coord
            mountain_pass.level = data['level'] if 'level' in data else mountain_pass.level


            mountain_pass.save()

            return Response({'status': 1, 'message': 'Запись успешно отредактирована в базе данных.'}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({'status': 400, 'message': 'Bad Request', 'id': None}, status=status.HTTP_400_BAD_REQUEST)


class GetUserMountainPassListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user__email',
                openapi.IN_QUERY,
                description="Введите email пользователя ...?user_email=<user@domain.com>",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: "OK - Success", 400: "Bad Request"},
    )
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('user__email', '')
        mountain_pass_list = MountainPass.objects.filter(user__email=email)
        serializer = MountainPassSerializer(mountain_pass_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

