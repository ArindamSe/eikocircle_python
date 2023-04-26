from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from authentication.utils import send_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = instance.request.build_absolute_uri(
        reverse('password_reset:reset-password-request')
    )
    data = {
        'name': reset_password_token.user.username,
        'link': f"{url}confirm/?token={reset_password_token.key}"
    }
    send_email(
        template_name="forgot_password_email.txt",
        data=data,
        subject="Password Reset for Eikomp",
        to=[reset_password_token.user.email]
    )
