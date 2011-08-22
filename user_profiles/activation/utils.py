from user_profiles.activation import settings as app_settings
from user_profiles.activation.models import ActivationCode
from user_profiles.utils import render_message, qualified_url
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

def require_activation_from_user(user, activation_code=None, set_user_inactive=False, profile_instance=None, created=False):
    """
    Deactivates a user account and requests activation from the user. You can
    call this function to re-request activation of a previously activated user
    account, for instance when users change their email address. To achieve
    this, you would typically write a handler for the ``User`` object's
    ``post_save`` signal. See the `relevant Django documentation
    <http://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.post_save>`_.

    
    .. note::
       If your user profile model has a ``deactivate`` method, it will be called
       by this function. Hence, if you need any specific code to be executed for
       deactivation of the user profile, you can simply implement its
       ``deactivate`` method.
       
    """
    if set_user_inactive:
        user.is_active = False
        user.save()
    profile_instance = profile_instance or user.get_profile()
    if hasattr(profile_instance, 'deactivate'):
        profile_instance.deactivate()
    send_activation_link_to_user(user, activation_code, created)
    
def accept_activation_code(activation_code):
    """
    Marks an ``ActivationCode`` object as used, and re-activates the associated
    user account.
    
    .. note::
       If your user profile model has an ``activate`` method, it will be called
       by this function. Hence, if you need any specific code to be executed for
       activation of the user profile, you can simply implement its ``activate``
       method.
    """
    activation_code.user.is_active = True
    activation_code.user.save()
    user_profile = activation_code.user.get_profile()
    if hasattr(user_profile, 'activate'):
        user_profile.activate()
    activation_code.activated = True
    activation_code.save()

def send_activation_link_to_user(user, activation_code=None, created=False):
    """
    Sends (and creates, if necessary) an activation code to the user passed. The
    ``created`` argument should be ``True`` if that user was just created.
    See :ref:_activation-templates.
    """
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
        'url': qualified_url(reverse('user_profiles_activate', args=[activation_code.key]), site),
        'form_url': qualified_url(reverse('user_profiles_activation_form'), site),
        'site_url': qualified_url('', site),
        'site': site,
        'key': activation_code.key,
        'user': user,
        'recipient': recipient,
        'profile': profile,
        'created': created,
    }
    subject = render_message('activation/email/activation_request.subject.txt',
        context_dict, remove_newlines=True)
    message = render_message('activation/email/activation_request.txt',
        context_dict)

    if app_settings.BY_EMAIL:
        send_mail(subject, message, None, [user.email], fail_silently=False)
