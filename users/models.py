from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxLengthValidator

from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel
from . import choices
from core import image_paths


User = get_user_model()


class Address(TimeStampedModel):
    street = models.CharField(max_length=250)
    building_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(
        max_length=3, choices=choices.GOVERNORATE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=250, default='Egypt')
    postal_code = models.IntegerField(blank=True, null=True)


class IDImages(TimeStampedModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=image_paths.id_image_path)


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=image_paths.profile_image_path, blank=True, null=True)
    # skills = relation with category
    about = models.TextField(verbose_name=_('About you'), )
    address = models.ForeignKey(
        Address, related_name='address', on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True, error_messages={
                                    'unique': _("A phone number already exists."), })
    transportation = models.CharField(
        max_length=1, choices=choices.TRANSPORTATION_CHOICES, null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=choices.GENDER_CHOICES, null=True, blank=True)
    id_number = models.IntegerField(validators=[MaxLengthValidator])
    id_images = models.ForeignKey(
        IDImages, related_name='id_images', on_delete=models.CASCADE)
    accept_terms = models.BooleanField(default=False)
    is_tasker = models.BooleanField(default=False)
