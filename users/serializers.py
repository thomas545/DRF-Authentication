from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from phonenumber_field.serializerfields import PhoneNumberField
from . import models

class RegisterUserSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone_number = PhoneNumberField(required=True, write_only=True, 
                            validators=[UniqueValidator(models.Profile.objects.all(), 
                            message=_("phone number already exist."))])

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    # def get_cleaned_data_profile(self):
    #     return {
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', ''),
    #         'phone_number': self.validated_data.get('phone_number', '')
    #     }

    def create_profile_data(self, user):
        # create profile data
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()
        user.profile.phone_number = self.validated_data.get('phone_number', '')
        user.profile.save()

    def custom_signup(self, request, user):
        self.create_profile_data(user)
