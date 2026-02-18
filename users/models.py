from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from courses.models import Course
from lessons.models import Lesson


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
    """описание модели пользователя"""

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


class Payment(models.Model):
    """описание модели о платежах пользователей по курсам и урокам"""

    CHOICES_PAYMENT_METHOD = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    date_payment = models.DateTimeField(default=now, verbose_name="Дата платежа")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="paid_course",
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name="paid_lesson",
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    sum_payment = models.FloatField(
        verbose_name="Сумма платежа", default=0.00, null=True, blank=True
    )
    payment_method = models.CharField(
        max_length=30,
        verbose_name="Способ оплаты",
        choices=CHOICES_PAYMENT_METHOD,
        default="Перевод на счет",
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        help_text="Укажите Id сессии",
        null=True,
        blank=True,
    )
    link = models.URLField(
        max_length=450,
        verbose_name="Cсылка на оплату",
        help_text="Укажите cсылку на оплату",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["date_payment"]
        unique_together = ["user", "paid_course", "paid_lesson"]
        indexes = [
            models.Index(fields=["user", "paid_course", "paid_lesson"]),
        ]

        def __str__(self):
            return (
                f"{self.user}"
                f"{self.date_payment}"
                f"{self.payment_method}"
                f" {self.sum_payment}"
            )
