import uuid
from shared.uitility import check_email_or_phone, send_email
from .models import User, UserConfirmation, VIA_EMAIL, VIA_PHONE_NUMBER,NEW, CODE_VERIFIED, DONE, PHOTO_STEP
from rest_framework import exceptions
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer,self).__init__(*args,**kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)


    class Meta:
        model = User
        fields = [
            'id',
            'auth_type',
            'auth_status',
        ]
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }


    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            print(code)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE_NUMBER:
            code = user.create_verify_code(VIA_PHONE_NUMBER)
            # send_phone_code(user.phone_number, code)
        user.save()
        return user


    def validate(self, data):
        super(SignUpSerializer,self).validate(data)
        data = self.auth_validate(data)
        return data
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        print(user_input,'++++++++++++')
        input_type = check_email_or_phone(user_input)
        if input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL,
            }
        elif input_type == 'phone_number':
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE_NUMBER,
            }
        else:
            data = {
                'success': False,
                'message': 'Invalid Email or Phone Number'
            }
            return ValidationError(data)
        print('data', data)
        return data
    def validate_email_phone_number(self, value):
        value = str(value).lower()
        # to do
        return value
    def to_representation(self, instance):
        print('to_rep', instance)
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(
            instance.token()
        )
        return data




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'user_roles',
            'auth_type',
            'auth_status',
            'email',
            'phone_number',
            'photo',
        ]

    def validate_email(self, value):
        value = value.lower()
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError(_("Invalid email format"))
        return value

    # def validate_phone_number(self, value):
    #     if not value.isdigit() or len(value) < 10:
    #         raise serializers.ValidationError(_("Invalid phone number format"))
    #     return value

    def validate(self, data):
        auth_type = data.get('auth_type')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if auth_type == VIA_EMAIL and not email:
            raise serializers.ValidationError(_("Email is required for VIA_EMAIL authentication"))

        if auth_type == VIA_PHONE_NUMBER and not phone_number:
            raise serializers.ValidationError(_("Phone number is required for VIA_PHONE_NUMBER authentication"))

        return data


