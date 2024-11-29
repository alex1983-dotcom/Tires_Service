import logging
import smtplib
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

# Настройка логирования
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Отправляет приветственное письмо новому пользователю после его регистрации.

    :param sender: Модель, которая вызвала сигнал (в данном случае User).
    :param instance: Экземпляр модели User, который был сохранен.
    :param created: Логическое значение, указывающее, был ли создан новый экземпляр.
    :param kwargs: Дополнительные параметры.
    """
    if created:
        subject = 'Добро пожаловать на наш сайт!'
        message = f'Здравствуйте, {instance.first_name} {instance.last_name},\n\nСпасибо за регистрацию на нашем сайте!'
        try:
            send_mail(subject, message, 'your_email@example.com', [instance.email])
            logger.info(f"Приветственное письмо успешно отправлено пользователю {instance.email}")
        except smtplib.SMTPException as smtp_e:
            logger.error(f"Ошибка SMTP при отправке письма пользователю {instance.email}: {smtp_e}")
        except Exception as e:
            logger.error(f"Не удалось отправить письмо пользователю {instance.email}: {e}")
