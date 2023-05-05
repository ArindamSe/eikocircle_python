from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Item_collected.views import ItemCollectedViewSet

router =  DefaultRouter()
router.register('', ItemCollectedViewSet, basename="Item-collected")

urlpatterns = [
    path('', include(router.urls)),
]
