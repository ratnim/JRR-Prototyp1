from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Address, PhoneNumber, Expert, State,  \
    Skills, UserMail, EmergencyContact, ContactInfo, Medical, Expertise

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


class MedicalSerializer(serializers.ModelSerializer):

    class Meta:
            model = Medical
            fields = ('details_medical_conditions', 'medical_conditions')


class ExpertiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expertise
        fields = ('expertise',)


class SkillsSerializer(serializers.ModelSerializer):
    expertise = ExpertiseSerializer(read_only=True)

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
        fields = ('mail',)


class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
            model = PhoneNumber
            fields = ('phone_number', 'type')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
            model = Address
            fields = ('address', 'postal_code', 'city', 'country')


class ContactInfoSerializer(serializers.ModelSerializer):

    address = AddressSerializer()
    user_mail = UserMailSerializer(many=True, read_only=True)
    phone_number = PhoneNumberSerializer(many=True, read_only=True)

    class Meta:
            model = ContactInfo
            fields = ('user_mail', 'phone_number', 'address')


class ProfileSerializer(serializers.ModelSerializer):

    contact_info = ContactInfoSerializer(read_only=True)
    emergency_contact = EmergencyContactSerializer(read_only=True)
    professional_info = SkillsSerializer(read_only=True)
    medical = MedicalSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'gender', 'date_of_birth',
                  'contact_info', 'professional_info', 'emergency_contact',
                  'medical', 'user')

    def update(self, instance, validated_data):

        self.set_personal_data(instance, validated_data.get('personal'))
        self.set_contact_data(instance, validated_data.get('contact'))
        self.set_medical_data(instance, validated_data.get('medical'))
        self.set_emergency_contact(instance, validated_data.get('emergency_contact'))
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


    def create_phone_list(self, phone_numbers, contact_info):
        for key in phone_numbers:
            match = PhoneNumber.objects.filter(phone_number=key['phone'], contact_info=contact_info)
            if not match:
                phone = PhoneNumber.objects.create(phone_number=key['phone'],
                                                   type=key['type'],
                                                   contact_info=contact_info)
                phone.save()


    def create_mail_list(self, mail_addresses, contact_info):
        for key in mail_addresses:
            match = UserMail.objects.filter(mail=key['email'], contact_info=contact_info)
            print(match , key['email'])
            if not match:
                mail = UserMail.objects.create(mail=key['email'], contact_info=contact_info)
                mail.save()


    def set_contact_data(self, instance, contact_data):
        address_data = contact_data.get('address')

        if instance.contact_info:
            instance.contact_info.address.address = address_data.get('address')
            instance.contact_info.address.postal_code = address_data.get('postal_code')
            instance.contact_info.address.city = address_data.get('city')
            instance.contact_info.address.country = address_data.get('country')

        else:
            address = Address.objects.create(
                address=address_data['address'],
                postal_code=address_data['postal_code'],
                city=address_data['city'],
                country=address_data['country'])
            address.save()
            contact = ContactInfo.objects.create(address=address)
            instance.contact_info = contact
            contact.save()

        self.create_mail_list(contact_data['emailset'], instance.contact_info)
        self.create_phone_list(contact_data['phoneset'], instance.contact_info)


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
                                        level_of_employment=skill_data['profession']['level_of_employment'],
                                        un_security_test=skill_data['profession']['un_security_test'],
                                        un_security_test_date=skill_data['profession']['un_security_test_date'],
                                        expertise=expertise)
            skills.save()
            instance.professional_info = skills


    def set_medical_data(self, instance, medical_info):
        if instance.medical:
            instance.medical.details_medical_conditions = medical_info['details_medical_conditions']
            instance.medical.medical_conditions = medical_info['medical_conditions']
        else:
            medic = Medical.objects.create(details_medical_conditions=medical_info['details_medical_conditions'],
                                           medical_conditions=medical_info['medical_conditions'])
            medic.save()
            instance.medical = medic

    def set_emergency_contact(self, instance, emergency_data):
        if instance.emergency_contact:
            instance.emergency_contact.name = emergency_data['name']
            instance.emergency_contact.relation = emergency_data['relation']
            instance.emergency_contact.phone = emergency_data['phone']
            instance.emergency_contact.email = emergency_data['email']
            instance.emergency_contact.city = emergency_data['city']
            instance.emergency_contact.country = emergency_data['country']
        else:
            contact = EmergencyContact.objects.create(name=emergency_data['name'],
                                                      relation=emergency_data['relation'],
                                                      phone=emergency_data['phone'],
                                                      email=emergency_data['email'],
                                                      city=emergency_data['city'],
                                                      country=emergency_data['country'])
            contact.save()
            instance.emergency_contact = contact


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('passed', 'available', 'id')
        extra_kwargs = {
            'passed': {'read_only': True},
            'available': {'read_only': True},
            'id': {'read_only': True},
        }


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
