from django.shortcuts import render
from django.views.generic import ListView
from .models import Ad, UserProfile, Response


class AdsList(ListView):
    model = Ad
    template_name = 'default.html'
    context_object_name = 'ads'
