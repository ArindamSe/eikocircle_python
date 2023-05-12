from django.urls import path, include
from rest_framework.routers import DefaultRouter

from collection_center.views import CollectionCenterViewSet, CollectedCenterItemCollectedViewSet

router = DefaultRouter()
router.register('center', CollectionCenterViewSet, basename='collection-center')
router.register('item', CollectedCenterItemCollectedViewSet, basename='collected-center-item')

urlpatterns = [
    path('', include(router.urls))
]
