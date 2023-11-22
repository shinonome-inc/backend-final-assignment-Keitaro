from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import CreateTweetForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateTweetForm
    template_name = "tweets/create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
