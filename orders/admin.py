
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem
from .resources import OrderResource, OrderItemResource


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)


@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('product__title',)
