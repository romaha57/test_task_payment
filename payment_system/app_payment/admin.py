from django.contrib import admin

from .models import Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'products', 'quantity', 'total_sum')
    search_fields = ('user',)
    list_filter = ('total_sum',)
    readonly_fields = ('total_sum',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
