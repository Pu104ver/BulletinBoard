from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import ResponseFilter
from .forms import ResponseForm, AdForm
from .models import Ad, Response


class AdsList(ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 6


class AdsDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        user_response = Response.objects.filter(ad=ad, user_profile=self.request.user.userprofile).first()
        context['user_response'] = user_response
        return context


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'user_ads.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(user_profile=self.request.user.userprofile)

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile
        return super().form_valid(form)


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    template_name = 'ad_create.html'
    form_class = AdForm
    success_url = reverse_lazy('my_posts')

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    template_name = 'ad_update.html'
    form_class = AdForm
    success_url = reverse_lazy('my_posts')

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile
        return super().form_valid(form)


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('my_posts')


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('my_responses')


class SubmitResponseView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        existing_response = Response.objects.filter(ad=ad, user_profile=request.user.userprofile).exists()
        if existing_response:
            return render(request, 'error.html', {'error_messages': 'Вы уже оставили отклик на это объявление.'})
        form = ResponseForm()
        return render(request, 'submit_response.html', {'ad': ad, 'form': form})

    def post(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        form = ResponseForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            existing_response = Response.objects.filter(ad=ad, user_profile=request.user.userprofile).exists()
            if existing_response:
                # Если отклик уже был - сообщение об ошибке
                messages.error(request, "Вы уже оставили отклик на это объявление.")
            else:
                response = Response(ad=ad, user_profile=request.user.userprofile, content=content)
                response.save()
                messages.success(request, "Отклик успешно добавлен.")

        return redirect('my_responses')


class MyResponsesListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'my_responses.html'
    context_object_name = 'responses'

    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().filter(user_profile=self.request.user.userprofile)
        return queryset.order_by('-created_at')


class MyResponsesToAdsListView(LoginRequiredMixin, FilterView):
    model = Response
    template_name = 'responses_to_me.html'
    context_object_name = 'responses'
    filterset_class = ResponseFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = Response.objects.filter(ad__user_profile=self.request.user.userprofile)
        return queryset.order_by('-created_at')

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            return redirect(request.path)
        return super().get(request, *args, **kwargs)


def accept_response(request, pk):
    response = get_object_or_404(Response, id=pk)
    if request.user.userprofile == response.ad.user_profile:
        if response.accepted:
            return render(request, 'error.html', {'error_messages': 'Отклик уже был принят.'})

        if request.method == 'POST':
            response.accepted = True
            response.save()
            return redirect('responses_to_my_ads')
        else:
            return render(request, 'accept_response.html', {'response': response})
    else:
        return render(request, 'access_denied.html')
