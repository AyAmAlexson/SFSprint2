from .models import *
from rest_framework import serializers


class PassImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = [
           'id',
           'data',
           'title',
        ]


class MountainPassSerializer(serializers.HyperlinkedModelSerializer):
    images = PassImageSerializer(many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = MountainPass
        fields = '__all__'

    def get_detail_url(self, obj):
        # Assuming 'get_mountain_pass' is the correct view name in your urlpatterns
        view_name = 'get_mountain_pass'
        request = self.context.get('request')
        return reverse(view_name, kwargs={'id': obj.pk}, request=request)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs, context=context)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


