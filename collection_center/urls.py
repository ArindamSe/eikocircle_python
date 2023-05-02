from django.urls import path, include
from rest_framework.routers import DefaultRouter

from collection_center.views import CollectionCenterViewSet

router = DefaultRouter()
router.register('', CollectionCenterViewSet, basename='collection-center')

urlpatterns = [
    path('', include(router.urls))
]
