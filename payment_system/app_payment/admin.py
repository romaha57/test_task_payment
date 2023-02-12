from django.contrib import admin

from .models import Discount, Item, Order, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tax', 'discount')
    list_editable = ('price',)
    search_fields = ('name',)
    readonly_fields = ('stripe_product_price_id',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'products', 'quantity', 'total_sum', 'tax', 'discount')
    search_fields = ('user',)
    list_filter = ('total_sum',)
    readonly_fields = ('total_sum',)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_id_for_stripe', 'value')
    search_fields = ('name',)
    readonly_fields = ('tax_id_for_stripe',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_id_for_stripe', 'value')
    search_fields = ('name',)
    readonly_fields = ('discount_id_for_stripe',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)
