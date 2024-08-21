from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import cloudinary
from cloudinary.models import CloudinaryField

# from business.models import Business  

# Create your models here.


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    user_code = models.CharField(max_length=50)
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    gender = models.CharField(max_length = 50)
    
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if not self.user_code:
            self.user_code = self._generate_user_code()
        super().save(*args, **kwargs)
    
    def _generate_user_code(self):
        last_id = User.objects.order_by('id').last()
        new_id = 1 if not last_id else last_id.id + 1
        return f'user{new_id:04d}'

    def __str__(self):
        return f'User {self.username} ({self.email})'
