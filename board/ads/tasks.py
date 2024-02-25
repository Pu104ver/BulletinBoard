from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from ads.models import Subscription


@shared_task
def task_send_hello_mail(username, email):
    subject = 'Добро пожаловать на наш сайт!'
    text = f'Привет, {username}! Спасибо за регистрацию на нашем сайте.'
    html = (
        f'<b>{username}</b>, вы успешно зарегистрировались на '
        f'<a href="http://127.0.0.1:8000/">сайте</a>!'
    )
    sender_email = None

    msg = EmailMultiAlternatives(subject, text, sender_email, [email])
    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def task_send_news_email(title, content):
    subscribed_users = Subscription.objects.values_list('user__email', flat=True)

    subject = title
    content = content

    html_content = render_to_string('email/news_notification.html', {'subject': subject, 'content': content})

    text_content = strip_tags(html_content)

    for email in subscribed_users:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def task_send_mail_to_the_author_of_the_response(user_profile, object_model):
    subject = 'Новый отклик на ваше объявление'
    message = f'Пользователь {user_profile.user.username} оставил отклик на ваше объявление "{object_model.title}".'
    sender_email = None
    recipient_email = object_model.user_profile.user.email  # Получатель письма - владелец объявления
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)


@shared_task
def task_send_mail_to_the_sender_of_the_response(user_profile, object_model):
    subject = 'Новый отклик с вашего аккаунта'
    message = (f'Вы получили это письмо, потому что с вашего аккаунта "{user_profile.user.username}" '
               f'был оставлен отклик на объявление "{object_model.title}".')
    sender_email = None
    recipient_email = user_profile.user.email  # Получатель письма - отправитель отклика
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)


@shared_task
def task_send_mail_to_response_creator_after_response_accepted(response):
    subject = 'Ваш отклик был принят'
    message = f'Автор объявления "{response.ad.title}" принял ваш отклик.'
    sender_email = None
    recipient_email = response.user_profile.user.email
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)


@shared_task
def task_send_mail_to_ad_creator_after_response_accepted(response):
    subject = 'Вы приняли отклик на ваше объявление'
    message = f'Вы успешно приняли отклик на ваше объявление "{response.ad.title}".'
    sender_email = None
    recipient_email = response.ad.user_profile.user.email
    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
