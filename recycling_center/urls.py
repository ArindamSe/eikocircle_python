from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recycling_center.views import RecyclingCenterViewSet, ItemRecycledViewSet

router = DefaultRouter()
router.register('details', RecyclingCenterViewSet, basename='recycling-center')
router.register('item-recycled', ItemRecycledViewSet, basename='item-recycled')

urlpatterns = [
    path('', include(router.urls))
]
