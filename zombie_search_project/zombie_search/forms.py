from django import forms
from django.contrib.auth.models import User
from zombie_search.models import Player

class UserForm(forms.ModelForm):
    password = forms.CharField(label = "Password", widget=forms.PasswordInput())
    confirm = forms.CharField(label = "Confirm Password", widget=forms.PasswordInput())

    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if not confirm:
            raise forms.ValidationError("Please confirm your password.")
        if confirm != password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

    class Meta:
        model = User
        fields = ('username', 'email','password','confirm')


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('profile_picture',)


class UpdateUser(forms.ModelForm):
    password = forms.CharField(label = "Current Password", widget=forms.PasswordInput(),required=False)
    new_password = forms.CharField(label = "New Password", widget=forms.PasswordInput(), required=False)
    confirm = forms.CharField(label = "Confirm Password", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('email','password','new_password','confirm')
