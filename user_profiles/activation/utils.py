from django.contrib.auth.models import User
from user_profiles.activation.models import ActivationCode
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import Context

def require_activation_from_user(user, activation_code=None, set_user_inactive=False):
    if set_user_inactive:
        user.is_active = False
        user.save()
    user_profile = user.get_profile()
    if hasattr(user_profile, 'deactivate'):
        user_profile.deactivate()
    send_activation_link_to_user(user, activation_code)
    
def accept_activation_code(activation_code):
    activation_code.user.is_active = True
    activation_code.user.save()
    user_profile = activation_code.user.get_profile()
    if hasattr(user_profile, 'activate'):
        user_profile.activate()
    activation_code.activated = True
    activation_code.save()

def qualified_url(path, site, scheme='http'):
    return '%(scheme)s://%(authority)s%(path)s' % {
        'scheme': scheme,
        'authority': site.domain,
        'path': path
    }

def send_activation_link_to_user(user, activation_code=None):
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
    }
    subject = get_template('activation/email/activation_request.subject.txt').render(Context(context_dict, autoescape=False)).replace('\n', '')
    message = get_template('activation/email/activation_request.txt').render(Context(context_dict, autoescape=False))
    send_mail(subject, message, None, [user.email], fail_silently=False)
