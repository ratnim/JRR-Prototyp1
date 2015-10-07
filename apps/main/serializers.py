from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Profile, Expert, State


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth',
                  'middle_name', 'address', 'postal_code', 'city',
                  'country', 'mail_address', 'main_profession',
                  'secondary_profession', 'level_of_employment',
                  'un_security_test', 'un_security_test_date',
                  'details_medical_conditions', 'medical_conditions',
                  'eme_name', 'eme_relation', 'eme_phone', 'eme_email',
                  'eme_city', 'eme_country')

    def update(self, instance, validated_data):
        # for key, value in validated_data.items():
        #    print(key)
        #    print(value)

        personal_information = validated_data.get('personal')

        instance.first_name = personal_information.get(
            'first_name', instance.first_name)
        instance.last_name = personal_information.get(
            'last_name', instance.last_name)
        instance.middle_name = personal_information.get(
            'middle_names', instance.middle_name)
        # instance.date_of_birth = personal_information.get(
        #    'date_of_birth', instance.date_of_birth)
        instance.gender = personal_information.get(
            'gender', instance.gender)

        self.set_contact_data(instance, validated_data)
        self.set_expertise_data(instance, validated_data)
        self.set_emergency_data(instance, validated_data)

        instance.save()
        return instance

    def set_contact_data(self, instance, validated_data):
        contact_data = validated_data.get('contact')

        # Fix this to be a List
        instance.mail_address = contact_data.get('emailset')[0].get('email')

        # Include type in this
        instance.phone_number = contact_data.get('phoneset')[0].get('phone')
        adress = contact_data.get('address')
        instance.address = adress.get('address')
        instance.postal_code = adress.get('postalCode')
        instance.city = adress.get('city')
        instance.country = adress.get('country')

    def set_expertise_data(self, instance, validated_data):
        skills = validated_data.get('skills')
        profession_info = skills.get('profession')
        for key in profession_info:
            setattr(instance, key, profession_info[key])
        instance.expertise = skills.get('expertise')[0].get(
            'expertise')

    def set_medical_data(self, instance, validated_data):
        medical_info = validated_data.get('medical')
        for key in medical_info:
            setattr(instance, key, medical_info[key])

    def set_emergency_data(self, instance, validated_data):
        emergency_contact = validated_data.get('emergency_contact')
        for key in emergency_contact:
            setattr(instance, 'eme_' + key, emergency_contact[key])


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

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile = ProfileSerializer()
    state = StateSerializer()

    class Meta:
        model = Expert
        fields = ('user', 'profile', 'state')


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
