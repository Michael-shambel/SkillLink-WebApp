from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class CustomUserManager(BaseUserManager):
    """
    This is a custom manager for your CustomUser model.
    Django uses managers to handle the creation
    and retrieval of model instances.
    By default, Django provides a manager for creating and managing users,
    but we use a custom manager to customize user creation.

    """
    def create_user(self, email, password, **extra_fields):
        """
        To create a regular user.
        save it in the database
        args:
            email: email of the user
            password: password of the user
        return:
            save to teh databse and return the user instance
            user
        """
        if not email:
            raise ValueError(_('The email field must be set'))
        if not password:
            raise ValueError(_('the password field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        To create a superuser (an admin user with elevated permissions).
        args:
            email: email for the stuff or superuser
            password: password of the user
            extra_fields: field for the stuff or superuser
        return
            user:
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model where email is the unique identifier.
    fields:
         The email address of the user, which is unique and used for login.
         Field for storing the password, but typically,
        you don't need to define this field manually
        because Django handles it internally.
        is_employer: A boolean field to specify if the user is an employer.
        is_job_seeker: A boolean field to specify if the user is a job seeker.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class JobSeekerProfile(models.Model):
    """
    this method will create a model for creating
    a model for job seeker profile
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="jobseeker_profile")

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    skills = models.TextField()
    experience = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployerProfile(models.Model):
    """
    this method will create a profile for a employer
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
