from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Ad(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
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

    def __str__(self):
        return f"Response to {self.ad} by {self.user_profile}"
