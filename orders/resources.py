from import_export import resources
from .models import Order, OrderItem

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'user__username', 'created_at', 'status')

class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem
        fields = ('id', 'order__id', 'product__name', 'quantity', 'price')
