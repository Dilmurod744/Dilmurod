from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.views import CategoryModelViewSet, ProductImageAPIView, ProductModelViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet, 'category')
router.register('product',ProductModelViewSet,'product')
urlpatterns = [
    path('', include(router.urls)),
    path('product/images/', ProductImageAPIView.as_view())
]







