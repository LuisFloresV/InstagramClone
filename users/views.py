"""User view"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.db.utils import IntegrityError
from .forms import ProfileForm, SignupForm
from django.contrib import messages
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from posts.models import Post


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add users posts"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


class SignupView(FormView):
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if request.user.is_authenticated:
            return redirect('posts:feed')
        return super().get(request, args, kwargs)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    model = Profile
    form_class = ProfileForm

    def get_object(self,):
        return self.request.user.profile

    def get_success_url(self):
        username = self.object.user.username
        return reverse_lazy('users:detail', kwargs={'username': username})

