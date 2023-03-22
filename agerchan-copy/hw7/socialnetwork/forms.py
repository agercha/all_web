from django import forms
from django.forms import widgets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from socialnetwork.models import *

MAX_UPLOAD_SIZE = 2500000

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic' )
        widgets = {
            'bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':'3'}),
            'profile_pic': forms.FileInput(attrs={'id': 'id_profile_picture'})
        }
        labels = {
            'bio': "",
            'profile_pic': "Upload Image"
        }

    def clean_picture(self):
        print(self.cleaned_data)
        profile_pic = self.cleaned_data['profile_pic']
        if not profile_pic or not hasattr(profile_pic, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not profile_pic.content_type or not profile_pic.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if profile_pic.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return profile_pic

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    username   = forms.CharField(max_length = 20)
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username