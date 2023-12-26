from .models import MountainPass, Image, User
from rest_framework.request import Request as DRFRequest
from .serializers import MountainPassSerializer

class MountainPassManager:
    @staticmethod
    def submit_data(cls, data, user_id, request=None):
        try:
            user = User.objects.get(pk=user_id)

            mountain_pass = MountainPass.objects.create(
                beauty_title=data['beauty_title'],
                title=data['title'],
                other_titles=data['other_titles'],
                connect=data['connect'],
                add_time=data['add_time'],
                user=user,
                coord=data['coords'],
                level=data['level']
            )

            for image_data in data['images']:
                Image.objects.create(
                    mountain_pass=mountain_pass,
                    data=image_data['data'],
                    title=image_data['title']
                )

            if request and isinstance(request, DRFRequest):
                context = {'request': request}
            else:
                context = {}
            serializer = MountainPassSerializer(mountain_pass, context=context)

            return {"status": 200, "message": "Отправлено успешно", "id": mountain_pass.id}

        except Exception as e:
            return {"status": 500, "message": str(e), "id": None}

class UserManager:
    @staticmethod
    def submit_data(cls, data, request=None):
        try:
            new_user = User.objects.create(
                email=data['email'],
                phone=data['phone'],
                name=data['name'],
                fam=data['fam'],
                otc=data['otc'],
            )
            

            if request and isinstance(request, DRFRequest):
                context = {'request': request}
            else:
                context = {}
            serializer = UserSerializer(new_user, context=context)

            return {"status": 200, "message": "Пользователь создан успешно", "id": new_user.id}

        except Exception as e:
            return {"status": 500, "message": str(e), "id": None}