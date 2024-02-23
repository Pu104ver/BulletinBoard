from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from .models import Response, Ad


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class AdForm(forms.ModelForm):
    content = RichTextUploadingField
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']


class UserAdsForm(forms.ModelForm):
    content = RichTextUploadingField
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']