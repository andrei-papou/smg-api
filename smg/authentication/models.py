from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = [
        'email',
        'phone',
        'skype',
        'birthday',
        'employment_date',
        'first_name',
        'last_name',
        'patronymic'
    ]

    phone = models.CharField(max_length=127, unique=True)
    skype = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(null=True)
    photo_large = models.ImageField(null=True)
    birthday = models.DateField()
    employment_date = models.DateField()
    patronymic = models.CharField(max_length=255)
    education = models.CharField(max_length=512, blank=True)

    department = models.ForeignKey('departments.Department', related_name='members', null=True)
    is_manager = models.BooleanField(default=False)

    def get_short_name(self):
        return '{} {}'.format(self.last_name, self.first_name)

    def get_full_name(self):
        return '{} {}'.format(self.get_short_name(), self.patronymic)

    @property
    def full_name(self):
        name = '{} {}'.format(self.get_short_name(), self.patronymic)
        return name

    @property
    def token(self):
        return self.auth_token.key
