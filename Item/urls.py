from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Item.views import ItemViewSet

router = DefaultRouter()
router.register('', ItemViewSet, basename='Item')

urlpatterns = [
    path('', include(router.urls)),
]
