from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
import stripe
from .models import Item, Order


class ItemDetailView(DetailView):
    model = Item
    template_name = 'app_payment/item_info.html'
    context_object_name = 'item'


class OrderDetailView(ListView):
    model = Order
    template_name = 'app_payment/order_info.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        orders = Order.objects.filter(user=self.request.user)
        total_price = 0
        for i in orders:
            total_price += i.total_sum

        context['total_price'] = total_price
        return context


class SuccessBuyView(TemplateView):
    template_name = 'app_payment/success.html'


class CancelBuyView(TemplateView):
    template_name = 'app_payment/cancel.html'


class BuyItemView(View):

    def get(self, request, *args, **kwargs):
        """Переопределяем post для работы со stripe(оплата заказа)"""

        item = Item.objects.get(id=self.kwargs.get('pk'))

        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': item.stripe_product_price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-cancel")}',
        )

        print(f'Session id для оплаты товара: {checkout_session.id}')

        return redirect(checkout_session.url, HTTPStatus.SEE_OTHER)


class BuyOrderView(View):

    def get(self, request, *args, **kwargs):
        """Переопределяем get для работы со stripe(оплата заказа)"""

        orders = Order.objects.filter(user=request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=orders.generate_line_items_for_stripe(),
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-cancel")}',
        )
        print(f'Session id для оплаты всего заказа: {checkout_session.id}')

        return redirect(checkout_session.url, HTTPStatus.SEE_OTHER)
