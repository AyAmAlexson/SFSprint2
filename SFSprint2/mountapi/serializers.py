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
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = MountainPass
        fields = '__all__'

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return reverse('get_mountain_pass', kwargs={'id': obj.pk}, request=request)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # If 'detail_url' is not already in the representation, add it
        if 'detail_url' not in ret:
            ret['detail_url'] = self.get_detail_url(instance)
        return ret

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs, context=context)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


