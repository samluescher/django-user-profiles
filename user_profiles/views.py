from user_profiles.utils import get_class_from_path, getattr_field_lookup
from user_profiles import settings as app_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.template import Template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404 
from django.core.exceptions import PermissionDenied
from django.contrib import messages

SIGNUP_SUCCESS_URL = None
SIGNUP_FORM_CLASS = get_class_from_path(app_settings.SIGNUP_FORM)
PROFILE_FORM_CLASS = get_class_from_path(app_settings.PROFILE_FORM)

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        signup_form = SIGNUP_FORM_CLASS(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            user_profile_form = PROFILE_FORM_CLASS(request.POST, instance=new_user.get_profile())
            try:
                user_profile_form.save()
                messages.success(request, _('Signup was successful. You can now log in.'))
                return HttpResponseRedirect(SIGNUP_SUCCESS_URL or reverse('login'))
            except Exception as e:
                # This should never happen. However, in case it ever should, delete unusable User:
                new_user.delete()
                raise e
    else:
        signup_form = SIGNUP_FORM_CLASS(initial=request.GET)
    context_dict = {
        'form': signup_form
    }
    return render_to_response('user_profiles/signup.html', 
        context_dict, context_instance=RequestContext(request))

def _user_detail(request, user):
    context_dict = {
        'user' : user
    }
    return render_to_response('user_profiles/profile/detail.html',
        context_dict, context_instance=RequestContext(request))

@login_required
def user_detail(request, lookup_value):
    kwargs = {app_settings.URL_FIELD: lookup_value}
    return _user_detail(request, get_object_or_404(User, **kwargs))

@login_required
def current_user_detail(request):
    return _user_detail(request, request.user)

def _user_change(request, user):
    if request.method == 'POST':
        try:
            profile = user.get_profile()
            form = PROFILE_FORM_CLASS(request.POST, instance=profile)
        except:
            form = PROFILE_FORM_CLASS(request.POST)        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Your changes were saved.'))
            if user != request.user:
                return HttpResponseRedirect(reverse('user_detail', args=[getattr_field_lookup(user, app_settings.URL_FIELD)]))
            else:
                return HttpResponseRedirect(reverse('current_user_detail'))
    else:
        try:
            profile = user.get_profile()
            form = PROFILE_FORM_CLASS(instance=profile)
        except:
            form = PROFILE_FORM_CLASS()
    
    context_dict = {
        'form' : form
    }
    
    return render_to_response('user_profiles/profile/change.html',
        context_dict, context_instance=RequestContext(request))

@login_required
def current_user_profile_change(request):
    return _user_change(request, request.user)