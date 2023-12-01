from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email: str, password: str) -> 'CustomUser':
        email = self.normalize_email(email)
        superuser = self.model(email=email, password=password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.set_password(password)
        superuser.save()
        return superuser
    
    def create_user(self, email: str, password: str, name: str, surname: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, name=name, surname=surname)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=30,
        default=''
    )
    surname = models.CharField(
        verbose_name='Surname',
        max_length=30,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Active',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Staff',
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name='Superuser',
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name='Date joined',
        default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'
    
    def save(self, *args, **kwags):
        if not self.name:
            self.name = f'User{self.pk}'
        super().save(*args, **kwags)
    
    