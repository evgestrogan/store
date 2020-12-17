from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from .validators import UnicodePhoneNumberValidator


class User(AbstractBaseUser, PermissionsMixin):
    """
    New user table with full name, phone number and products
    """
    username_validator = UnicodeUsernameValidator()
    phone_number_validator = UnicodePhoneNumberValidator()

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text='Необходимые. 150 символов или меньше. Только буквы, цифры и @ /. / + / - / _.',
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
    )
    number_phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=9,
        validators=[phone_number_validator],
        help_text='Обязательное поле. Не более 9 символов. Только цифры не считая кода',
    )
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150)
    email = models.EmailField(verbose_name='email адрес')
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now)
    is_staff = models.BooleanField(
        verbose_name='Статус администратора',
        default=False,
        help_text='Определяет, может ли пользователь войти на этот сайт администратора.',
    )
    is_active = models.BooleanField(
        verbose_name='Статус аккаунта',
        default=True,
        help_text='Определяет, следует ли рассматривать этого пользователя как активного. ' +
                  'Снимите этот флажок вместо удаления учетных записей.',
    )
    # product = models.ManyToManyField(
    #     'systemStore.Product',
    #     verbose_name='Корзина',
    #     related_name='user',
    # )
    product = models.ManyToManyField(
        "systemStore.Product",
        through='DescriptionProductUser',
        through_fields=('user', 'product'),
        verbose_name='Корзина',
        related_name='user',
    )
    # product = models.ManyToManyField('systemStore.Product',
    #                                  through='systemStore.Order',
    #                                  through_fields=('user', 'product'))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'number_phone', 'last_name', 'first_name', 'middle_name', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        """Returns the username."""
        return self.username


class DescriptionProductUser(models.Model):
    """
    Смежная таблица между продуктом и пользователем.
    Используется для хранения количества продукта
    и связи двух таблиц m2m
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_to_product',
    )
    product = models.ForeignKey(
        "systemStore.Product",
        on_delete=models.CASCADE,
        related_name='product_to_user',
    )
    count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )