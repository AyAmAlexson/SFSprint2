from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .managers import MountainPassManager, UserManager
from .serializers import MountainPassSerializer
from .models import *
import json
from django.shortcuts import get_object_or_404

class SubmitDataView(APIView):
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
            mountain_pass.coord = data['coords'] if 'coords' in data else mountain_pass.coords
            mountain_pass.level = data['level'] if 'level' in data else mountain_pass.level


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

