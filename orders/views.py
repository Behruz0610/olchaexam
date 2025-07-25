from rest_framework import viewsets, filters, status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'items__product__name']
    ordering_fields = ['id', 'created_at', 'status']

    def get_queryset(self):
        # Faqat o'zining zakazlarini ko'rsin va optimizatsiya
        return Order.objects.select_related('user').prefetch_related('items__product').filter(user=self.request.user)

    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get('status')
        if status_value not in dict(order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        return Response({'status': order.status})
