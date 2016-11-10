from rest_framework import serializers
from rest_api.models import Service, App
from django.contrib.auth.models import User


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Service
        fields = ('url', 'name', 'owner', 'origin_url', 'instance_num', 'created')


class AppSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    service = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = App
        fields = ('url', 'name', 'owner', 'service', 'ip', 'port', 'cat', 'state', 'sub')
