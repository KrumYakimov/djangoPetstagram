from django.contrib.auth.views import LogoutView
from django.urls import path, include
from petstagram.accounts import views

urlpatterns = [
    path("login/", views.AppUserLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register/", views.AppUserRegisterView.as_view(), name="register"),
    path(
        "profile/<int:pk>/",
        include(
            [
                path("", views.AppUserDetailView.as_view(), name="profile-details"),
                path("edit/", views.ProfileEditView.as_view(), name="profile-edit"),
                path("delete/", views.ProfileDeleteView.as_view(), name="profile-delete"),
            ]
        ),
    ),
]
