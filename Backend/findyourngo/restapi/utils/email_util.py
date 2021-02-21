from django.core.mail import send_mail


def send_email(subject, message, sender_email, receiver_email):
    send_mail(
        subject,
        message,
        sender_email,
        [receiver_email],
        fail_silently=False,
    )