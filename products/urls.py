from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CommentViewSet, FavoriteViewSet, ProductReviewViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
router.register('reviews', ProductReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
