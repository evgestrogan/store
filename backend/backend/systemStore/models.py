from django.db import models


class Category(models.Model):
    """Model category for product"""
    title = models.CharField(
        verbose_name='Название категории',
        max_length=150,
        unique=True,
        help_text='Обязательное поле. Не более 150 символов.',
        error_messages={
            'unique': 'Категория с таким названием уже существует',
        },
    )

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.title


class Product(models.Model):
    """Model for product"""
    title = models.CharField(
        verbose_name='Название продукта',
        max_length=150,
        unique=True,
        help_text='Обязательное поле. Не более 150 символов.',
        error_messages={
            'unique': 'Продукт с таким названием уже существует',
        },
    )
    description = models.TextField(
        verbose_name='Описание продукта',
        help_text='Поле ввода описаие продукта',
    )
    vendor_code = models.CharField(
        verbose_name='Артикул продукта',
        max_length=50,
        help_text='Обязательное поле. Не более 50 символов.',
    )
    weight = models.DecimalField(
        verbose_name='Вес продукта',
        max_digits=5,
        decimal_places=3,
        help_text='Обязательное поле веса продукта. в формате (xx.xxx)',
    )
    price = models.DecimalField(
        verbose_name='Цена продукта',
        max_digits=5,
        decimal_places=2,
        help_text='Обязательное поле цены продукта. в формате (xxx.xx)',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория продукта',
        help_text='Выбор категории продукта для отображения в строке названия товара',
        related_name='product',
    )
    presence = models.BooleanField(
        verbose_name='Наличие продукта',
        default=False,
        help_text='Поле отображающее наличие товара',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class ProductPhoto(models.Model):
    """
    Таблица для хранения фотографий продуктов
    """
    photo = models.ImageField(
        upload_to='photo',
        verbose_name='Фото продукта',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='photo',
    )

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фотографии продуктов'

    def __str__(self):
        return self.photo.name


class Order(models.Model):
    """
    Таблица заказа
    """

    TYPE_CHOICES = (
        ('О', 'В обработке'),
        ('П', 'Подтвержден'),
        ('З', 'Завершен'),
    )

    user = models.ForeignKey(
        'systemAuthentication.User',
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
    )
    product = models.ManyToManyField(
        Product,
        through='DescriptionProductOrder',
        through_fields=('order', 'product'),
        verbose_name='Продукт',
        related_name='order',
    )
    status = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Статус заказа',
        default='О',
    )
    created = models.DateTimeField(
        verbose_name='Время создания заказа',
        help_text='Дата и время подачи заявки на офрмление заказа',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_count_products(self):
        return sum([p.count for p in self.order_to_product.all()])


class DescriptionProductOrder(models.Model):
    """
    Смежная таблица между заказом и продуктом.
    Используется для хранения количества продукта
    и связи двух таблиц m2m
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_to_product',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_to_order',
    )
    count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )