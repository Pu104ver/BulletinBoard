from django import forms
from django.contrib import admin
from ckeditor_uploader.fields import RichTextUploadingField


from .models import UserProfile, Ad, Response, News, Subscription


class AdAdminForm(forms.ModelForm):
    content = RichTextUploadingField()

    class Meta:
        model = Ad
        fields = '__all__'


admin.site.register(UserProfile)
admin.site.register(Ad)
admin.site.register(Response)
admin.site.register(News)
admin.site.register(Subscription)
