from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Profile, Expert
from datetime import datetime


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'allow_null': True}
        }


class ExpertSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=False, many=False)

    class Meta:
        model = Expert
        fields = ('user', 'profile')


class ExpertRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    user = UserSerializer()

    class Meta:
        model = Expert
        fields = ('profile', 'user', )

    def create(self, validated_data):
        return Expert.experts.create(
            username=validated_data['user']['username'],
            email=validated_data['user']['email'],
            password=validated_data['user']['password'],
            date_joined=validated_data['user']['date_joined'] or datetime.now(),
            name=validated_data['profile']['name'],
        )


class SuperuserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'allow_null': True}
        }

    def create(self, validated_data):
        dateJoined = validated_data['date_joined'] or datetime.now()

        superuser = User(
            email=validated_data['email'],
            username=validated_data['username'],
            date_joined=dateJoined,
            is_staff=True,
            is_superuser=True
        )
        superuser.set_password(validated_data['password'])
        superuser.save()
        return superuser

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True,
            validators=[validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_joined', 'password'
                  )
        read_only_fields = ('date_joined', )

    def to_representation(self, obj):
        returnObj = super(UserSerializer, self).to_representation(obj)

        # if isinstance(self.context['request'].user, Account):
        if self.context['request'].user.id == obj.id:
            newObj = {
                'email': obj.email
            }
            returnObj.update(newObj)
        return returnObj

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        instance.save()

        if self.checkPassword(validated_data):
            instance.set_password(validated_data.get('password'))
            instance.save()

        return instance
