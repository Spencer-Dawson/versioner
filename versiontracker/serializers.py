from django.db.models import fields
from rest_framework import serializers
from .models import AppEnvironment, AppName, AppVersion

class AppEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppEnvironment
        fields = (['env_name'])

class AppNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppName
        fields = (['app_name'])


class AppVersionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.app_name', read_only=True)
    environment = serializers.CharField(source='environment.env_name', read_only=True)
    class Meta:
        model = AppVersion
        fields = (['name', 'environment', 'version', 'deploy_date'])

class AppNameRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance.app_name

    def to_representation(self, value):
        return value.app_name

    def to_internal_value(self, data):
        return AppName.objects.get(app_name=data)

class AppEnvironmentRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance.env_name

    def to_representation(self, value):
        return value.env_name

    def to_internal_value(self, data):
        return AppEnvironment.objects.get(env_name=data)


class AppVersionDeserializer(serializers.ModelSerializer):
    #name and environment as objects based on input string
    name = AppNameRelatedField(queryset=AppName.objects.all())
    environment = AppEnvironmentRelatedField(queryset=AppEnvironment.objects.all())
    class Meta:
        model = AppVersion
        fields = (['name', 'environment', 'version'])
