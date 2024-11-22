from django.contrib.auth import get_user_model, login, views as auth_view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from petstagram.accounts.forms import AppUserCreationForm, ProfileEditForm
from petstagram.accounts.models import Profile
from petstagram.accounts.signals import send_welcome_email, send_welcome_email_to_user
from petstagram.utils.mixins import UserIsOwnerMixin

UserModel = get_user_model()


class AppUserLoginView(auth_view.LoginView):
    template_name = "accounts/login-page.html"
    redirect_authenticated_user = True


class AppUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "accounts/register-page.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.save()
                # print(f"User {user.email} created successfully.")  # Debugging
                login(self.request, user)
                return HttpResponseRedirect(self.success_url)
        except Exception as e:
            print(f"Error during registration: {e}")
            raise


# class AppUserDetailView(views.DetailView):
#     queryset = Profile.objects.all()
#     template_name = "accounts/profile-details-page.html"

class AppUserDetailView(LoginRequiredMixin, views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('photo_set__like_set', 'pet_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        counts = self.object.photo_set.aggregate(
            total_likes_count=Count('like__id'),
            total_photos_count=Count('id'),
        )
        context['total_likes_count'] = counts['total_likes_count'] or 0
        context['total_photos_count'] = counts['total_photos_count']

        context['total_pets_count'] = self.object.pet_set.count()

        context['pets'] = self.object.pet_set.all()
        context['photos'] = self.object.photo_set.all()

        return context


class ProfileEditView(LoginRequiredMixin, UserIsOwnerMixin, views.UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile-edit-page.html"

    def get_success_url(self):
        return reverse_lazy(
            "profile-details",
            kwargs={"pk": self.object.pk}
        )


class ProfileDeleteView(LoginRequiredMixin, UserIsOwnerMixin, views.DeleteView):
    model = Profile
    template_name = "accounts/profile-delete-page.html"
    success_url = reverse_lazy("login")
