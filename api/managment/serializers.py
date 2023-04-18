from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Doctor, DoctorVisit, Guardian, Patient, PatientSetting, Tariff, Tranzaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        patient = super().create(validated_data)
        return patient

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_serializer = self.fields['user']
            user_serializer.update(instance.user, validated_data['user'])
            validated_data.pop('user')

        return super().update(instance, validated_data)


class GuardianSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    care_about = PatientSerializer(read_only=True)

    class Meta:
        model = Guardian
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        guard = super().create(validated_data)
        return guard

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_serializer = self.fields['user']
            user_serializer.update(instance.user, validated_data['user'])
            validated_data.pop('user')

        return super().update(instance, validated_data)


class PatientSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSetting
        fields = "__all__"


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class TranzactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tranzaction
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['patient'] = instance.patient
        return super().update(instance, validated_data)

    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class DoctorVisitViewOnlySerializer (serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = DoctorVisit
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class DoctorVisitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['patient'] = instance.patient
        return super().update(instance, validated_data)

    class Meta:
        model = DoctorVisit
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class ReadOnlyDoctorVisitSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = DoctorVisit
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class ChangePasswordSerializer(serializers.Serializer):
    password_old = serializers.CharField(max_length=128, min_length=8)
    password_new = serializers.CharField(max_length=128, min_length=8)

    def validate_password_old(self, password_old):
        if not self.instance.check_password(password_old):
            raise ValidationError('Old password is not correct')
        return password_old

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password_new'])
        instance.save()
        return instance
