from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        """To create normal user"""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            # Normalize the email address. If user insert upper case, it will be converted to lower case.
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """To create superuser"""
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # Because I have set USERNAME_FIELD email address instead of username to authenticate the user that's why I don't need to specify it in the require fields. And of course password is required.
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    # Informing this model that we are using MyAccountManager class to create normal user and super user..
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # REQUIRED METHODS for the AbstractUser class

    def has_perm(self, perm, obj=None):
        return self.is_admin    # If user is admin then he has all the permissions.

    def has_module_perms(self, app_label):
        return True
