from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(Group.objects.get(name='managers').user_set.all())
        user = User.objects.get(username='abc')
        permissions = user.get_all_permissions()
        print(permissions)
