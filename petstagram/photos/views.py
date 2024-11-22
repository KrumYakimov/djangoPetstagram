from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from petstagram.common.forms import CommentForm
from petstagram.pets.views import PetAddPage
from petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from petstagram.photos.models import Photo
from petstagram.utils.mixins import UserIsOwnerMixin


class PhotoAddPage(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'photos/photo-add-page.html'
    form_class = PhotoAddForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user

        return super().form_valid(form)


class PhotoEditPage(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    # def dispatch(self, request, *args, **kwargs):
    #     photo = self.get_object()
    #     if photo.user != request.user:
    #         return render(request, '403.html', status=403)  # Render a custom 403 template
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('photo-details', kwargs={'pk': self.object.pk})


@login_required
def photo_delete(request, pk: int):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user != request.user:
        return render(request, '403.html', status=403)

    photo.delete()
    return redirect('home')


class PhotoDetailsView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()

        return context
