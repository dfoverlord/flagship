from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

"""
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)
"""        

"""
class UserInformationUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'company', 'website',)
"""        

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        
class UserInformationUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email',)
        
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('company', 'website', 'short_bio','image',)