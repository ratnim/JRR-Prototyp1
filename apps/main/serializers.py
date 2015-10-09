from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Address, PhoneNumber, Expert, State, EmergencyContact, Expertise, Skills, UserMail, ContactInfo


class ExpertiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expertise
        fields = ('expertise')


class Skills(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('expertise', 'main_profession', 'secondary_profession',
                  'level_of_employment', 'un_security_test',
                  'un_security_test_date', 'expertise')


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
        fields = ('name', 'relation', 'phone', 'email',
                  'city', 'country')


class UserMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMail
        fields = ('mail')


class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
            model = PhoneNumber
            fields = ('phone_number')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
            model = Address
            fields = ('address', 'postal_code', 'city', 'country')


class ContactInfoSerializer(serializers.ModelSerializer):

    class Meta:
            model = Address
            fields = ('mail_addresses', 'phone_numbers', 'address')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'gender', 'date_of_birth',
                  'contact_info', 'professional_info', 'emergency_contact',
                  'details_medical_conditions', 'medical_conditions')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            print(key)
            print(value)

        self.set_personal_data(instance, validated_data.get('personal'))
        self.set_contact_data(instance, validated_data.get('contact'))
        self.set_medical_data(instance, validated_data.get('medical'))
        #self.set_emergency_contact(instance, validated_data.get('emergency_contact'))
        self.set_expertise_data(instance, validated_data.get('skills'))

        instance.save()
        return instance


    def set_personal_data(self, instance, personal_information):
        instance.name = personal_information.get(
            'name', instance.name)
        instance.surname = personal_information.get(
            'surname', instance.surname)
        instance.date_of_birth = personal_information.get(
            'date_of_birth', instance.date_of_birth)
        instance.gender = personal_information.get(
            'gender', instance.gender)



    def set_contact_data(self, instance, contact_data):
        # Fix this to be a List
        address_data = contact_data.get('address')

        if instance.contact_info:
            instance.contact_info.mail_addresses = contact_data.get('emailset')[0].get('email')

        # Include type in this
            instance.contact_info.phone_numbers = contact_data.get('phoneset')[0].get('phone')
            instance.contact_info.address = address_data.get('address')
            instance.contact_info.postal_code = address_data.get('postalCode')
            instance.contact_info.city = address_data.get('city')
            instance.contact_info.country = address_data.get('country')

        else:
            address = Address.objects.create(address=address_data['address'],
                                             postal_code=address_data['postal_code'],
                                             city=address_data['city'],
                                             country=address_data['country'])
            address.save()
            phone_number = PhoneNumber.objects.create(phone_number=contact_data['phoneset'][0].get('phone'))
            phone_number.save()
            mail = UserMail.objects.create(mail=contact_data['emailset'][0].get('mail'))
            mail.save()
            contact = ContactInfo.objects.create(mail_addresses=mail,
                                       phone_numbers=phone_number,
                                       address=address)
            contact.save()
            instance.contact_info = contact

        instance.save()


    def set_expertise_data(self, instance, skill_data):
        if instance.professional_info:
            profession_info = skill_data.get('profession')
            for key in profession_info:
                setattr(instance.professional_info, key, profession_info[key])
            instance.professional_info.expertise.expertise = skill_data.get('expertiseset')[0].get(
                'expertise')
        else:
            expertise = Expertise.objects.create(expertise=skill_data.get('expertiseset')[0].get(
                'expertise'))
            expertise.save()

            skills = Skills.objects.create(main_profession=skill_data['profession']['main_profession'],
                                        secondary_profession=skill_data['profession']['secondary_profession'],
                                        level_of_deployment=skill_data['profession']['level_of_employment'],
                                        un_security_test=skill_data['profession']['un_security_test'],
                                        un_security_test=skill_data['profession']['un_security_test_date'],
                                        expertise=expertise)
            skills.save()
            instance.professional_info = skills
        instance.save()


    def set_medical_data(self, instance, medical_info):
        for key in medical_info:
            setattr(instance, key, medical_info[key])
        print('medical done')


    def set_emergency_contact(self, instance, emergency_data):
        for key in emergency_data:
            setattr(instance, key, emergency_data[key])
        print('emergency done')


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
