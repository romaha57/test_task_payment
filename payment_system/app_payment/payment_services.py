import stripe
from django.conf import settings
from django.urls import reverse_lazy


def get_discount_value(data, is_item=None, is_order=None):
    """Получаем значение скидки для товара/заказа"""

    if is_item:
        if data.discount:
            discount = [{
                'coupon': data.discount.discount_id_for_stripe,
            }]

            return discount

    elif is_order:
        if data.check_discount():
            discount = [{
                'coupon': data.check_discount().discount_id_for_stripe,
            }]

            return discount


def _create_checkout_session(line_items_data, discount):
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items_data,
        mode='payment',
        discounts=discount,
        success_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-success")}',
        cancel_url=f'{settings.DOMAIN_NAME}{reverse_lazy("app_payment:buy-cancel")}',
    )

    print(f'Session id для оплаты товара: {checkout_session.id}')

    return checkout_session


def create_checkout_session(data, is_item=None, is_order=None):
    """ Получаем checkout session для платежной системы stripe """

    if is_item:
        discount = get_discount_value(data, is_item=True)
        line_items_data = [{
                'price': data.stripe_product_price_id,
                'quantity': 1,
                'tax_rates': [data.tax.tax_id_for_stripe],
            }]

        return _create_checkout_session(line_items_data=line_items_data, discount=discount)

    if is_order:

        discount = get_discount_value(data, is_order=True)
        line_items_data = data.generate_line_items_for_stripe()

        return _create_checkout_session(line_items_data=line_items_data, discount=discount)
