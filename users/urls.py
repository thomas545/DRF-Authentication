"""taskkez URL Configuration"""
from django.views.generic import TemplateView
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LoginView



router = routers.DefaultRouter()


urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('rest-auth/', include('rest_auth.urls')),
    path('registration/', views.RegisterUserView.as_view(), name='account_signup'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account-confirm-email/sent/', TemplateView.as_view(), name='account_email_verification_sent'),
    path('account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
]

