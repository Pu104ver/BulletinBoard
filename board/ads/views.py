from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Ad, UserProfile, Response


class AdsList(ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'


class AdsDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'
