from django.urls import path, include
from rest_framework.routers import DefaultRouter

from awareness_plan.views import AwarenessPlanViewSet, AwarenessPlanPicsViewSet

router = DefaultRouter()
router.register('plan', AwarenessPlanViewSet, basename='awareness-plan')
router.register('pics', AwarenessPlanPicsViewSet, basename='awareness-plan-pics')

urlpatterns = [
    path('', include(router.urls))
]
