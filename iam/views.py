from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _

from .forms import SignUpForm, UserInformationUpdateForm, ProfileForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

"""
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'my_profile.html'
    success_url = reverse_lazy('my_profile')
    
    def get_object(self):
        return self.request.user
"""

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserInformationUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            success_url = reverse_lazy('my_profile')
            return redirect(success_url)
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserInformationUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
    