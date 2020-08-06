from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ContactForm(forms.Form):
    name= forms.CharField(max_length=500, label="Name")
    email= forms.EmailField(max_length=500, label="Email")
    # comment= forms.CharField(max_length=500, label="Message")
    comment= forms.CharField(label='',widget=forms.Textarea(
                    attrs={'placeholder': 'Enter your message here...'}))
