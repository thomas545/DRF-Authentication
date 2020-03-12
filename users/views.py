from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import JWTSerializer
from rest_auth.utils import jwt_encode
from allauth.account.utils import complete_signup
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from rest_framework.response import Response
from rest_framework import status


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class RegisterUserView(RegisterView):

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        email = EmailAddress.objects.get(user=user, email=user.email)
        print("email ->>" , email)
        confirmation = EmailConfirmationHMAC(email)
        print("key ->>>", confirmation.key)
        # TODO send email confirmation here
        return user
