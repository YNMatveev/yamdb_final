from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    role = models.TextField('Роль', choices=Role.choices, default=Role.USER)
    bio = models.TextField('Биография', max_length=500, blank=True)
    email = models.EmailField('Почтовый адрес', unique=True)
    confirmation_code = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.role == User.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.Role.MODERATOR or self.is_admin

    @property
    def confirmation_code(self):
        return default_token_generator.make_token(self)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


@receiver(pre_save, sender=User)
def superuser_is_admin(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.role = User.Role.ADMIN
