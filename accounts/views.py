from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import ProcessFormView

from mysite.settings import LOGIN_REDIRECT_URL
from tweets.models import Tweet

from .forms import SignupForm
from .models import User


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/profile.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tweets"] = Tweet.objects.filter(user=self.request.user)
        return context


class FollowView(LoginRequiredMixin, ProcessFormView, TemplateView):
    template_name = "accounts/follow.html"

    def get(self, request, *args, **kwargs):
        context = {
            "username": kwargs["username"],
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)
        followee = get_object_or_404(User, username=kwargs["username"])
        if user == followee:
            return HttpResponseBadRequest()
        else:
            user.followee.add(followee)
            return redirect("tweets:home")


class UnFollowView(LoginRequiredMixin, ProcessFormView, TemplateView):
    template_name = "accounts/unfollow.html"

    def get(self, request, *args, **kwargs):
        context = {
            "username": kwargs["username"],
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)
        followee = get_object_or_404(User, username=kwargs["username"])
        if user == followee:
            return HttpResponseBadRequest()
        else:
            user.followee.remove(followee)
            return redirect("tweets:home")


class FolloweeView(LoginRequiredMixin, ListView):
    template_name = "accounts/followee.html"
    model = User


class FollowerView(LoginRequiredMixin, ListView):
    template_name = "accounts/follower.html"
    model = User
