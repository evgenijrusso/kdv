from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ Пользователь """
    code = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Code'))  # доп. поле для user
