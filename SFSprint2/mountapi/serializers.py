from .models import *
from rest_framework import serializers
from rest_framework.reverse import reverse

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
    url = serializers.HyperlinkedIdentityField(
        view_name='get_mountain_pass',  # Make sure this matches the name in urlpatterns
        lookup_field='pk'
    )
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='get_mountain_pass',  # Make sure this matches the name in urlpatterns
        lookup_field='pk'
    )

    class Meta:
        model = MountainPass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs, context=context)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


