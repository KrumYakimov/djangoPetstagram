from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from petstagram.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(auth_forms.UserCreationForm):
    # Override Labels by Redefining Fields
    # password1 = forms.CharField(
    #     label="Choose a Password",
    #     widget=forms.PasswordInput,
    #     help_text="Your password must be at least 8 characters long."
    # )
    # password2 = forms.CharField(
    #     label="Confirm Your Password",
    #     widget=forms.PasswordInput,
    #     help_text="Re-enter the same password for verification."
    # )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ("email",)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)



