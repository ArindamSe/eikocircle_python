from django.urls import path, include
from rest_framework.routers import DefaultRouter

from brand_product.views import BrandProductViewSet

router =  DefaultRouter()
router.register('', BrandProductViewSet, basename="Brand-Product")

urlpatterns = [
    path('', include(router.urls)),
]
