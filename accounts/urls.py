
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CustomObtainPairView, LogoutView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView




router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
