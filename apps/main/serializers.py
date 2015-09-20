from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Profile, Expert, State


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'id')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('passed', 'available', 'id')
        extra_kwargs = {
            'passed': {'read_only': True},
            'available': {'read_only': True},
            'id': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'date_joined', 'id')
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
        }


class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile = ProfileSerializer()
    state = StateSerializer()

    class Meta:
        model = Expert
        fields = ('user', 'profile', 'state')


def validate_email(data):
    """Validate that the email of the user is not used yet"""
    email = data['email']
    user = User.objects.get(email=email)

    if (user is not None):
        raise serializers.ValidationError('A user with the email {0} already exists.'.format(email))

    return data


class ExpertRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    user = UserSerializer(validators=[validate_email])


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
