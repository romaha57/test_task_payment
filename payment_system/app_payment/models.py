import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY


class Item(models.Model):
    """ Модель для товара """

    name = models.CharField(max_length=100, verbose_name='название товара')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цена')
    stripe_product_price_id = models.CharField(max_length=128, verbose_name='price id для stripe',
                                               null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.CASCADE, verbose_name='налог', null=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE,
                                 verbose_name='скидка', null=True, blank=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """При сохранении формы добавляем в поле у товара его stripe_product_price_id """

        if not self.stripe_product_price_id:
            stripe_price = self.get_stripe_price()
            self.stripe_product_price_id = stripe_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_stripe_price(self):
        """Функция для получения stripe_price, чтобы потом получить stripe_product_price_id"""

        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency="rub"
        )
        return stripe_price


class OrderQuerySet(models.QuerySet):
    """ Переопределяем менеджер для обращения ко всем заказам """

    def generate_line_items_for_stripe(self):
        """ Формироуем line_items для stripe.checkout.Session.create() """

        line_items = []
        for order in self:
            item = {
                'price': order.products.stripe_product_price_id,
                'quantity': order.quantity,
                'tax_rates': [order.tax.tax_id_for_stripe],
            }
            line_items.append(item)

        return line_items

    def check_discount(self):
        """Проверяем есть ли в заказах пользователя скидка"""

        for order in self:
            if order.discount:
                return order.discount

        return False


class Order(models.Model):
    """Модель заказа"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    products = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='товар в заказе')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='количество')
    total_sum = models.PositiveIntegerField(default=0, verbose_name='сумма заказа')
    tax = models.ForeignKey('Tax', on_delete=models.CASCADE, verbose_name='налог', null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE,
                                 verbose_name='скидка', null=True, blank=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return str(self.user)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """При сохранении формы считает общую сумму товара с учетом количества """

        total_sum = self.products.price * self.quantity
        self.total_sum = total_sum
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Tax(models.Model):
    """ Модель налога """

    name = models.CharField(max_length=255, verbose_name='название налога')
    description = models.TextField(verbose_name='описание', null=True)
    value = models.PositiveSmallIntegerField(default=0, verbose_name='величина налога')
    tax_id_for_stripe = models.CharField(max_length=128,
                                         verbose_name='id для checkout.session', null=True)

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """ При сохранении формы создаем tax_id для подсчета налога """

        tax = stripe.TaxRate.create(
            display_name="Sales Tax",
            inclusive=True,
            percentage=18,
        )
        self.tax_id_for_stripe = tax.id
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Discount(models.Model):
    """ Модель скидки """

    name = models.CharField(max_length=255, verbose_name='название скидки')
    description = models.TextField(verbose_name='полное описание')
    value = models.PositiveSmallIntegerField(default=0, verbose_name='величина скидки')
    discount_id_for_stripe = models.CharField(max_length=128, verbose_name='id для checkout.session')

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """При сохранении формы создаем discount_id для подсчета скидки """

        discount = stripe.Coupon.create(percent_off=self.value, duration="once")
        self.discount_id_for_stripe = discount.id
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
