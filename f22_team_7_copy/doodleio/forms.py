from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, label="", widget=forms.TextInput(attrs={'placeholder': 'Enter Name'}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        user = authenticate(username=username,password="")
        if User.objects.select_for_update().filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # if not user:
        #     raise forms.ValidationError("Invalid username")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class GuessForm(forms.Form):
    guess = forms.CharField(max_length = 20, label="Enter guess")
