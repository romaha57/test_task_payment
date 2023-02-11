from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='название товара')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цена')
    stripe_product_price_id = models.CharField(max_length=128, verbose_name='price id для stripe',
                                               null=True, blank=True)

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
    def generate_line_items_for_stripe(self):
        line_items = []
        for order in self:
            item = {
                'price': order.products.stripe_product_price_id,
                'quantity': order.quantity,

            }
            line_items.append(item)
        return line_items


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    products = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='товар в заказе')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='количество')
    total_sum = models.PositiveIntegerField(default=0, verbose_name='сумма заказа')

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

