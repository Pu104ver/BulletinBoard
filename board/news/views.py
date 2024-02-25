from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, ListView, DetailView

from ads.models import News, Subscription
from news.forms import NewsForm


class NewsListView(ListView):
    model = News
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 6


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('ads.add_news',)
    model = News
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'


@login_required
@csrf_protect
def subscriptions(request):
    user_subscribed = Subscription.objects.filter(user=request.user).exists()
    print(f'{user_subscribed=}')
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.get_or_create(user=request.user)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user).delete()

        return redirect('subscriptions')

    return render(
        request,
        'subscriptions.html',
        {'user_subscribed': user_subscribed}
    )
