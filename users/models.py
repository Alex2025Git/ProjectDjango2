from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Необходимо указать Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="email address")
    token = models.CharField(
        max_length=110, verbose_name="Токен", blank=True, unique=True, null=True
    )
    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    phone_number = models.CharField(
        max_length=35,
        unique=True,
        verbose_name="phone number",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    nik_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Ваш Ник",
        blank=True,
        null=True,
        help_text="Укажите Ник",
    )
    avatar = models.ImageField(
        upload_to="avatar",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
