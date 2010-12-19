from user_profiles.activation import settings as app_settings
from user_profiles.activation.models import ActivationCode
from user_profiles.utils import render_message, qualified_url
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

def require_activation_from_user(user, activation_code=None, set_user_inactive=False, profile_instance=None, created=False):
    if set_user_inactive:
        user.is_active = False
        user.save()
    profile_instance = profile_instance or user.get_profile()
    if hasattr(profile_instance, 'deactivate'):
        profile_instance.deactivate()
    send_activation_link_to_user(user, activation_code, created)
    
def accept_activation_code(activation_code):
    activation_code.user.is_active = True
    activation_code.user.save()
    user_profile = activation_code.user.get_profile()
    if hasattr(user_profile, 'activate'):
        user_profile.activate()
    activation_code.activated = True
    activation_code.save()

def send_activation_link_to_user(user, activation_code=None, created=False):
    if not activation_code:
        ActivationCode.objects.filter(user=user, activated=False).delete()
        activation_code = ActivationCode(user=user)
        activation_code.save()

    try:
        site = Site.objects.get_current()
    except Site.DoesNotExist:
        site = Site(domain='<unknown>', name='<unknown>')
    domain = site.domain
    profile = user.get_profile()
    if profile and profile.__unicode__():
        recipient = profile
    else:
        recipient = user
    context_dict = {
        'url': qualified_url(reverse('user_profiles_activation_activate', args=[activation_code.key]), site),
        'form_url': qualified_url(reverse('user_profiles_activation_form'), site),
        'site_url': qualified_url('', site),
        'site': site,
        'key': activation_code.key,
        'user': user,
        'recipient': recipient,
        'profile': profile,
        'created': created,
    }
    subject = render_message('activation/email/activation_request.subject.txt', context_dict, remove_newlines=True)
    message = render_message('activation/email/activation_request.txt', context_dict)

    if app_settings.BY_EMAIL:
        send_mail(subject, message, None, [user.email], fail_silently=False)
