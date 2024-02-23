from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Response


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Response)
def send_notifications(sender, instance, created, **kwargs):
    if created:
        # Уведомление автора об отклике на его объявление
        send_mail_to_the_author_of_the_response(instance.user_profile, instance.ad)
        # Уведомление отправителя о новом отклике с его аккаунта
        send_mail_to_the_sender_of_the_response(instance.user_profile, instance.ad)


def send_mail_to_the_author_of_the_response(user_profile, object_model):
    subject = 'Новый отклик на ваше объявление'
    message = f'Пользователь {user_profile.user.username} оставил отклик на ваше объявление "{object_model.title}".'
    sender_email = None
    recipient_email = user_profile.user.email  # Получатель письма - владелец объявления
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)


def send_mail_to_the_sender_of_the_response(user_profile, object_model):
    subject = 'Новый отклик с вашего аккаунта'
    message = (f'Вы получили это письмо, потому что с вашего аккаунта "{user_profile.user.username}" '
               f'был оставлен отклик на объявление "{object_model.title}".')
    sender_email = None
    recipient_email = user_profile.user.email  # Получатель письма - владелец объявления
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
