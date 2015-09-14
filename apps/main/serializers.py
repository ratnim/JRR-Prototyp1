from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=False, many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')


class UserRegistrationDeserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        dateJoined = validated_data['date_joined']
        if not dateJoined:
            dateJoined = datetime.now()

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            date_joined=dateJoined
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
