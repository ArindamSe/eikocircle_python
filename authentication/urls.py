from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import ChangePasswordView, LoginView, RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name="registration"),
    path('login', LoginView.as_view(), name="login"),
    path('refresh', TokenRefreshView.as_view(), name="token_refresh"),

    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
