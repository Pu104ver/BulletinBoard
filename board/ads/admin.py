from django.contrib import admin

from .models import UserProfile, Ad, Response

admin.site.register(UserProfile)
admin.site.register(Ad)
admin.site.register(Response)

