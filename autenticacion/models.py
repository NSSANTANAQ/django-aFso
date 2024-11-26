from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core import validators
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#


# Create your models here.
class Usuario(AbstractBaseUser):
    username = models.CharField(('Usuario'), max_length=200, unique=True, blank=False, validators=[
        RegexValidator(
            regex='^[a-z0-9_-]*$',
            message='Usernames can only contain letters, numbers, underscores, and dashes.'
        )
    ])

    email = models.EmailField(
        verbose_name='Correo',
        max_length=255,
        unique=True,
        validators=[validators.validate_email]
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    estado = models.IntegerField(default=1)
    departamento = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    def __str__(self):
        return '{}{}{}'.format(self.username, " ", self.email," " ,self.departamento)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = "usuario"
        verbose_name = "usuario"
        verbose_name_plural = 'usuarios'
        ordering = ['username']
