from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='email')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label="password", strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="confirm password", strip=False, required=True,
                                       widget=forms.PasswordInput)
    email = forms.EmailField(label="email", required=True, widget=forms.EmailInput)
    username = forms.CharField(required=True, label="username")
    avatar = forms.ImageField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "password_confirm", "first_name", "last_name", "email", "avatar",
                  "birthday",)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password_confirm and password and password !=password_confirm:
            raise ValidationError("Пароли не совпадают")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "avatar",
                  "birthday")


class InstaSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="find")