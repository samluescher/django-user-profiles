from user_profiles.utils import get_class_from_path, getattr_field_lookup
from user_profiles import settings as app_settings
from user_profiles.signals import post_signup
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.template import Template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
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
            if user_profile_form.is_valid():
                user_profile_form.save()
                if new_user.is_active:
                    messages.success(request, _('Signup was successful. You can now proceed to log in.'))
                else:
                    messages.success(request, _('Signup was successful. Activation ist required before you can proceed to log in.'))
                post_signup.send(__name__, user=new_user)
                return HttpResponseRedirect(SIGNUP_SUCCESS_URL or reverse('login'))
            else:
                # This should not happen, unless the user profile form can't be validated
                # with the data validated using the POST form.
                new_user.delete()
                raise Exception("Form '%s' could be validated, while '%s' couldn't. Please make sure the two classes are compatible. Validation errors were: %s" % 
                    (signup_form.__class__.__name__, user_profile_form.__class__.__name__, user_profile_form.errors.as_text()))
    else:
        signup_form = SIGNUP_FORM_CLASS(initial=request.GET)
    context_dict = {
        'form': signup_form
    }
    return render_to_response('user_profiles/signup.html', 
        context_dict, context_instance=RequestContext(request))

def _user_detail(request, user, extra_context={}):
    context_dict = {
        'user' : user,
        'profile': user.get_profile(),
    }
    context_dict.update(extra_context)
    return render_to_response('user_profiles/profile/detail.html',
        context_dict, context_instance=RequestContext(request))

@login_required
def user_detail(request, lookup_value, extra_context={}):
    kwargs = {app_settings.URL_FIELD: lookup_value}
    try:
        user = User.objects.get(**kwargs)
        return _user_detail(request, user, extra_context)
    except (User.DoesNotExist, ValueError):
        raise Http404

@login_required
def current_user_detail(request, extra_context={}):
    return _user_detail(request, request.user, extra_context)

def _user_change(request, user):
    if request.method == 'POST':
        try:
            profile = user.get_profile()
            form = PROFILE_FORM_CLASS(request.POST, instance=profile)
        except:
            form = PROFILE_FORM_CLASS(request.POST)        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('Your changes were saved.'))
            if user != request.user:
                return HttpResponseRedirect(reverse('user_detail', args=[getattr_field_lookup(user, app_settings.URL_FIELD)]))
            else:
                return HttpResponseRedirect(reverse('current_user_detail'))
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        try:
            profile = user.get_profile()
            form = PROFILE_FORM_CLASS(instance=profile)
        except:
            form = PROFILE_FORM_CLASS()
    
    context_dict = {
        'form' : form,
        'profile' : profile,
    }
    
    return render_to_response('user_profiles/profile/change.html',
        context_dict, context_instance=RequestContext(request))


def logout_then_login(request, **kwargs):
    result = auth_views.logout_then_login(request, **kwargs)
    messages.info(request, _('You have been logged out.'))
    return result
    
@login_required
def current_user_profile_change(request):
    return _user_change(request, request.user)
    
@login_required
def redirect_to_current_user_detail(request):
    return HttpResponseRedirect(reverse('current_user_detail'))

@csrf_protect
@login_required
def password_change(request, **kwargs):
    """
    Wraps the `contrib.auth` view, redirecting to the user profile page with a user message when done.
    """
    if not kwargs.get('post_change_redirect'):
        kwargs['post_change_redirect'] = reverse('current_user_detail') 
    result = auth_views.password_change(request, **kwargs)
    if isinstance(result, HttpResponseRedirect):
        messages.info(request, _('Your password was changed.'))
    return result

# Doesn't need csrf_protect since no-one can guess the URL
def password_reset_confirm(request, **kwargs):
    """
    Wraps the `contrib.auth` view, redirecting to the login page with a user message when done.
    """
    if not kwargs.get('post_reset_redirect'):
        kwargs['post_reset_redirect'] = reverse('login') 
    result = auth_views.password_reset_confirm(request, **kwargs)
    if isinstance(result, HttpResponseRedirect):
        messages.info(request, _('Your password has been set.  You may go ahead and log in now.'))
    return result
