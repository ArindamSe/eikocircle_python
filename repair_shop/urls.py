from django.urls import path, include
from rest_framework.routers import DefaultRouter

from repair_shop.views import RepairShopViewSet

router =  DefaultRouter()
router.register('', RepairShopViewSet, basename="repair-shop")

urlpatterns = [
    path('', include(router.urls)),
]
