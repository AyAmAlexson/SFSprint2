from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .managers import MountainPassManager
from .serializers import MountainPassSerializer
from .models import *
import json
from django.shortcuts import get_object_or_404

class SubmitDataView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')

            if not user_id:
                return Response({'status': 400, 'message': 'Bad Request', 'id': None}, status=status.HTTP_400_BAD_REQUEST)

            result = MountainPassManager.submit_data(data, user_id)
            return Response(result, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({'status': 400, 'message': 'Bad Request', 'id': None}, status=status.HTTP_400_BAD_REQUEST)

class GetMountainPassView(APIView):
    def get(self, request, id, *args, **kwargs):
        mountain_pass = get_object_or_404(MountainPass, pk=id)
        serializer = MountainPassSerializer(mountain_pass)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditMountainPassView(APIView):
    def patch(self, request, id, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')

            if not user_id:
                return Response({'status': 400, 'message': 'Bad Request', 'id': None}, status=status.HTTP_400_BAD_REQUEST)

            mountain_pass = get_object_or_404(MountainPass, pk=id)


            if mountain_pass.status != 'new':
                return Response({'status': 0, 'message': 'Нельзя редактировать запись в статусе, отличном от "new".'}, status=status.HTTP_400_BAD_REQUEST)


            mountain_pass.beauty_title = data['beauty_title']
            mountain_pass.title = data['title']
            mountain_pass.other_titles = data['other_titles']
            mountain_pass.connect = data['connect']
            mountain_pass.coord = data['coords']
            mountain_pass.level = data['level']


            mountain_pass.save()

            return Response({'status': 1, 'message': 'Запись успешно отредактирована в базе данных.'}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({'status': 400, 'message': 'Bad Request', 'id': None}, status=status.HTTP_400_BAD_REQUEST)


class GetUserMountainPassListView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('user__email', '')
        mountain_pass_list = MountainPass.objects.filter(user__email=email)
        serializer = MountainPassSerializer(mountain_pass_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
