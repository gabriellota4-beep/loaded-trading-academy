from django import forms

from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'trading_experience', 'preferred_market']
