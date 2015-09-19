from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Profile, Expert, Status


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'date_joined', 'id')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('passed', 'available')


class ExpertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expert
        fields = ('user', 'profile', 'status')


class ExpertRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    user = UserSerializer()

    class Meta:
        model = Expert
        fields = ('profile', 'user')

    def create(self, validated_data):
        return Expert.experts.create(
            email=validated_data['user']['email'],
            password=validated_data['user']['password'],
            first_name=validated_data['profile']['first_name'],
            last_name=validated_data['profile']['last_name']
        )
