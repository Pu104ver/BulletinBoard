from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile, Response, News, Subscription
from .tasks import task_send_hello_mail, task_send_news_email, task_send_mail_to_the_sender_of_the_response, \
    task_send_mail_to_the_author_of_the_response, task_send_mail_to_ad_creator_after_response_accepted, \
    task_send_mail_to_response_creator_after_response_accepted


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        common_users = Group.objects.get_or_create(name="common users")
        if not common_users:
            instance.groups.add(common_users)
        task_send_hello_mail(instance.username, instance.email)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=News)
def send_news_notification(sender, instance, created, **kwargs):
    if not created:
        return
    task_send_news_email(instance.title, instance.content)


@receiver(post_save, sender=Response)
def send_response_notifications(sender, instance, created, **kwargs):
    if created:
        # Уведомление автора об отклике на его объявление
        task_send_mail_to_the_author_of_the_response(instance.user_profile, instance.ad)

        # Уведомление отправителя о новом отклике с его аккаунта
        task_send_mail_to_the_sender_of_the_response(instance.user_profile, instance.ad)

    if instance.accepted:
        # Отправка уведомления тому, кто принял отклик
        task_send_mail_to_ad_creator_after_response_accepted(instance)

        # Отправка уведомления тому, кто создал отклик
        task_send_mail_to_response_creator_after_response_accepted(instance)
