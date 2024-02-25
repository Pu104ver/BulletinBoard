from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


class Ad(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    category_choices = [
        ('TANKS', 'Танки'),
        ('HEALERS', 'Хилы'),
        ('DAMAGE_DEALERS', 'ДД'),
        ('TRADESMEN', 'Торговцы'),
        ('GUILD_MASTERS', 'Гилдмастеры'),
        ('QUEST_GIVERS', 'Квестгиверы'),
        ('BLACKSMITHS', 'Кузнецы'),
        ('LEATHERWORKERS', 'Кожевники'),
        ('ALCHEMY_MASTERS', 'Зельевары'),
        ('SPELLCASTERS', 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=30, choices=category_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.id)])


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.user_profile}]: {self.ad}"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return self.user.username
