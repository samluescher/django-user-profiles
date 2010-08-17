from django import template
from django.utils.translation import ugettext_lazy as _

def salutation(title, last_name, first_name=''):
    values = {'first_name': first_name, 'last_name': last_name}
    if title == 'MRS':
        return _('Dear Mrs %(last_name)s,') % values
    elif title == 'MS':
        return _('Dear Ms %(last_name)s,') % values
    elif title == 'FAMILY':
        return _('Dear %(last_name)s family,') % values
    else:
        return _('Dear Mr %(last_name)s,') % values

register = template.Library()
register.simple_tag(salutation)
