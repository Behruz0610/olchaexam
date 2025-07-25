from rest_framework import viewsets, filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer, FavoriteSerializer
from .models import Favorite
from rest_framework.permissions import IsAuthenticated
from .models import ProductReview
from .serializers import ProductReviewSerializer
# ProductReview uchun ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ProductReview.objects.select_related('user', 'product').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Favorite uchun ViewSet
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, BasePermission

# Custom permission: faqat o'z commentini update/delete qilish
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.user == request.user

# Comment uchun ModelViewSet
from .models import Comment

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'product').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'user__username', 'product__name']
    ordering_fields = ['id', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




# Optimization va search/filter/order qo'shilgan ProductViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('comments__user').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'price', 'created_at']

    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  

    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


