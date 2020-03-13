"""taskkez URL Configuration"""
from django.views.generic import TemplateView
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LogoutView

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginUserView.as_view(), name='account_login'),
    path('password/change/', views.PasswordChangeView.as_view(), name='rest_password_change'),
    path('password/reset/', views.PasswordResetUserView.as_view(), name='rest_password_reset'),
    path('', include('rest_auth.urls')),
    path('registration/', views.RegisterUserView.as_view(), name='account_signup'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account-confirm-email/<str:key>/', views.VerifyUserEmailView.as_view(), name='account_confirm_email'),
    path('password/reset/confirm/<str:uid>/<str:token>/', views.PasswordResetConfirmUserView.as_view(), name='rest_password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),

]

