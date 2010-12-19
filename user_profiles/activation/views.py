from user_profiles.activation.models import ActivationCode
from user_profiles.activation.utils import require_activation_from_user, accept_activation_code
from user_profiles.activation.signals import post_activation
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

class ActivationForm(forms.Form):
    key = forms.CharField(label=_('Activation code'), required=True)

def activate(request, key=None):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        key = request.POST.get('key', None)
    else:
        if key:
            form = ActivationForm({'key': key})
        else:
            form = ActivationForm()

    if form.is_valid():
        key = form.cleaned_data['key']
        try:
            activation_code = ActivationCode.objects.get(key=key)
            if activation_code.activated:
                messages.error(request, _('This activation code has already been used.'))
            else:
                accept_activation_code(activation_code)
                if not request.user.is_authenticated():
                    messages.success(request, _('Thank you, activation was successful. You can now proceed to log in.'))
                else:
                    messages.success(request, _('Thank you, activation was successful.'))
                    post_activation.send(__name__, user=activation_code.user)
            if request.user == activation_code.user:
                return HttpResponseRedirect(reverse('current_user_detail'))
            else:
                return HttpResponseRedirect(settings.LOGIN_URL)
        except ActivationCode.DoesNotExist:
            messages.error(request, _('This is not a valid activation code.'))
            form = ActivationForm()

    return render_to_response('activation/form.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def current_user_send(request):
    try:
        activation_code = ActivationCode.objects.filter(user=request.user, activated=False)[0]
    except IndexError:
        activation_code = None
    require_activation_from_user(request.user, activation_code)
    success_message = _('An activation code has been sent to your email address: %(email)s. Please click the link in the email in order to activate.') % {
        'email': request.user.email
    }
    messages.success(request, success_message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', settings.LOGIN_REDIRECT_URL))
    