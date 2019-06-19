import urllib
import urllib.request
import json

from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _

from .forms import SignUpForm, UserInformationUpdateForm, ProfileForm

'''
LOGGING
'''
import logging
from django.http import HttpResponse

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        #logger.info('%s %s', 'recaptcha_response: ', recaptcha_response)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        #logger.info('%s %s', 'data: ', data)
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        #logger.info('%s %s', 'result: ', result)
        
        if (not result['success']) or (not result['action'] == 'signup'):
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return form_invalid(form)
        ''' End reCAPTCHA validation '''
        
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pages:home')
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form': form})


'''
Use django login flow, with added logic for google recaptcha
'''
class MyLoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('pages:home')
   
    def form_valid(self, form):
        request_body = self.request.POST
        if not request_body:
            return None
        
        #logger.info('%s %s', 'request_body: ', request_body)
        
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request_body.get('g-recaptcha-response')
        #logger.info('%s %s', 'recaptcha_response: ', recaptcha_response)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        #logger.info('%s %s', 'data: ', data)
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        #logger.info('%s %s', 'result: ', result)
        ''' End reCAPTCHA validation '''
        
        # result will be a dict containing 'success' and 'action'.
        # it is important to verify both
        if (not result['success']) or (not result['action'] == 'login'):
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return super().form_invalid(form)
            return redirect('login')
        
        auth_login(self.request, form.get_user())
        return super().form_valid(form)


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
    
    