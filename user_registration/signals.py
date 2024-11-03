import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать на наш сайт!'
        message = f'Здравствуйте, {instance.first_name} {instance.last_name},\n\nСпасибо за регистрацию на нашем сайте!'
        try:
            send_mail(subject, message, 'your_email@example.com', [instance.email])
            logger.info(f"Приветственное письмо успешно отправлено пользователю {instance.email}")
        except Exception as e:
            logger.error(f"Не удалось отправить письмо пользователю {instance.email}: {e}")
