from django.urls import path, include
from rest_framework.routers import DefaultRouter

from awareness_plan.views import AwarenessPlanViewSet

router = DefaultRouter()
router.register('', AwarenessPlanViewSet, basename='awareness-plan')

urlpatterns = [
    path('', include(router.urls))
]
