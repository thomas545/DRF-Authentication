from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics, views, exceptions

from rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import JWTSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer
from rest_auth.utils import jwt_encode
from allauth.account.utils import complete_signup
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from rest_auth.views import LoginView
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LogoutView, PasswordChangeView, PasswordResetConfirmView
from . import serializers, models


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
        confirmation = EmailConfirmationHMAC(email)
        print("key ->>>", confirmation.key)
        # TODO send email confirmation here
        return user

class LoginUserView(LoginView):
    queryset = ''

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class VerifyUserEmailView(VerifyEmailView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        # for updating email address
        email_confirm = confirmation.email_address
        user = email_confirm.user
        user_email = EmailAddress.objects.filter(user=user)
        
        if email_confirm.verified and user_email.count() > 1:
            EmailAddress.objects.filter(email=user.email).delete()
            user_email.update(primary=True)
            User.objects.filter(pk=user.pk).update(email=email_confirm.email)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


class PasswordResetUserView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.NotAcceptable(_("please enter correct email."))
        # TODO send email
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        uid = urlsafe_base64_encode(force_bytes(user.pk))#.decode('utf-8')
        token = default_token_generator.make_token(user)
        print("password/reset/confirm/" + uid + "/" + token)
        return Response({"detail": _("Password reset has been sent.")}, 
                        status=status.HTTP_200_OK)


class PasswordResetConfirmUserView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmUserView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Password has been reset with the new password.")})


class PasswordUserChangeView(PasswordChangeView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been Changed.")})


class UserDetailsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()
