from django.urls import path

from .views import ItemDetailView, OrderDetailView, SuccessBuyView, CancelBuyView, BuyItemView, BuyOrderView

app_name = 'app_payment'

urlpatterns = [
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_info'),
    path('order/<str:username>', OrderDetailView.as_view(), name='order_info'),
    path('buy/<int:pk>', BuyItemView.as_view(), name='buy-item'),
    path('buy/<str:username>', BuyOrderView.as_view(), name='buy-order'),
    path('buy-success/', SuccessBuyView.as_view(), name='buy-success'),
    path('buy-cancel/', CancelBuyView.as_view(), name='buy-cancel'),
]
