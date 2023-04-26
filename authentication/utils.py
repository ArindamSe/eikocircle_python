from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(subject, template_name, data, to, from_email=None, message=None):
    template = get_template(template_name)
    content = message or template.render(data)
    try:
        send_mail(
            # title:
            subject=subject,
            # message:
            message=content,
            # from:
            from_email=from_email or "noreply@somehost.local",
            # to:
            recipient_list=to
        )
    except Exception as e:
        print(repr(e))
