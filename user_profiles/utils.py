from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import SiteProfileNotAvailable
from django.db import models
from django.utils.importlib import import_module

def get_user_profile_model():
    """
    Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.
    """
    from django.conf import settings
    if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
        raise SiteProfileNotAvailable('You need to set AUTH_PROFILE_MO'
                                      'DULE in your project settings')
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    except ValueError:
        raise SiteProfileNotAvailable('app_label and model_name should'
                ' be separated by a dot in the AUTH_PROFILE_MODULE set'
                'ting')

    try:
        model = models.get_model(app_label, model_name)
        if model is None:
            raise SiteProfileNotAvailable('Unable to load the profile '
                'model, check AUTH_PROFILE_MODULE in your project sett'
                'ings')
        return model
    except (ImportError, ImproperlyConfigured):
        raise SiteProfileNotAvailable

def get_class_from_path(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
    try:
        func = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a class "%s"' % (module, attr))
    return func

def getattr_field_lookup(obj, lookup):
    path = lookup.split('__')
    attr = path.pop()
    for item in path:
        manager = getattr(obj, item+'_set')
        obj = manager.all()[0]
    return getattr(obj, attr)
