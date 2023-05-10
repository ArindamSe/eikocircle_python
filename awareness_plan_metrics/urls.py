from django.urls import path, include
from rest_framework.routers import DefaultRouter

from awareness_plan_metrics.views import AwarenessPlanMetricsViewSet

router = DefaultRouter()
router.register('', AwarenessPlanMetricsViewSet, basename='awareness-plan-metrics')

urlpatterns = [
    path('', include(router.urls))
]
