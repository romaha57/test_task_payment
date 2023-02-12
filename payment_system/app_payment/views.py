from http import HTTPStatus

from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from .models import Item, Order
from .payment_services import create_checkout_session


class ItemDetailView(DetailView):
    model = Item
    template_name = 'app_payment/item_info.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.discount:
            context['price_with_discount'] = \
                self.object.price - (self.object.price * self.object.discount.value / 100)

        return context


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
        discount = 0
        if orders.check_discount():
            discount = orders.check_discount().value

        for i in orders:
            total_price += i.total_sum

        context['total_price'] = total_price
        context['total_price_with_discount'] = total_price - (total_price * discount / 100)
        context['discount'] = discount

        return context


class SuccessBuyView(TemplateView):
    template_name = 'app_payment/success.html'


class CancelBuyView(TemplateView):
    template_name = 'app_payment/cancel.html'


class BuyItemView(View):

    def get(self, request, *args, **kwargs):
        """Переопределяем post для работы со stripe(оплата заказа)"""

        item = Item.objects.get(id=self.kwargs.get('pk'))
        checkout_session = create_checkout_session(item, is_item=True)

        return redirect(checkout_session.url, HTTPStatus.SEE_OTHER)


class BuyOrderView(View):

    def get(self, request, *args, **kwargs):
        """Переопределяем get для работы со stripe(оплата заказа)"""

        orders = Order.objects.filter(user=request.user)
        checkout_session = create_checkout_session(orders, is_order=True)

        return redirect(checkout_session.url, HTTPStatus.SEE_OTHER)
