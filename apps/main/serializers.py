from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Expert, State, EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
            model = EmergencyContact
            fields = ('name', 'relation', 'phone', 'email',
                      'city', 'country')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'gender', 'date_of_birth',
                  'contact_info', 'professional_info', 'emergency_contact',
                  'details_medical_conditions', 'medical_conditions')

    def update(self, instance, validated_data):
        # for key, value in validated_data.items():
        #    print(key)
        #    print(value)

        personal_information = validated_data.get('personal')

        instance.name = personal_information.get(
            'name', instance.name)
        instance.surname = personal_information.get(
            'surname', instance.surname)
        # instance.date_of_birth = personal_information.get(
        #    'date_of_birth', instance.date_of_birth)
        instance.gender = personal_information.get(
            'gender', instance.gender)

        self.set_contact_data(instance, validated_data)
        self.set_expertise_data(instance, validated_data)

        emergency_contact_data = validated_data.get('emergency_contact')
        instance.emergency_contact = EmergencyContact.objects.create(
            **emergency_contact_data)

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
            name=validated_data['profile']['name'],
            surname=validated_data['profile']['surname']
        )
