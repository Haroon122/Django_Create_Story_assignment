from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'bio')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 