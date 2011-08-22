from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.db import models
from django.utils.importlib import import_module
from django.template.loader import get_template
from django.template import Context
from django.utils.text import normalize_newlines
from django.conf import settings

_user_profile_model_cache = None

def get_user_profile_model():
    """
    Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.
    """
    global _user_profile_model_cache
    if _user_profile_model_cache:
        return _user_profile_model_cache
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
        # There is an issue with sphinx_build not being able to import the 
        # profile model. Simply ignore the error in this case. 
        if model is None and not getattr(settings, 'IS_SPHINX_BUILD_DUMMY', False):
            raise SiteProfileNotAvailable('Unable to load the profile '
                'model, check AUTH_PROFILE_MODULE in your project sett'
                'ings')
        _user_profile_model_cache = model
        return model
    except (ImportError, ImproperlyConfigured):
        raise SiteProfileNotAvailable

def create_profile_for_new_user(user):
    # For internal use only: Creates a profile instance for a new user instance
    model = get_user_profile_model()
    instance = model(user=user)
    sync_profile_fields(user, instance)
    instance.save()
    return instance

def sync_profile_fields(from_instance, to_instance):
    # For internal use only: Copies fields with the same name between model
    # instances of arbitrary classes.
    changed_fields = []
    for field_name in from_instance._meta.get_all_field_names():
        try:
            field = to_instance._meta.get_field(field_name)
            new_value = getattr(from_instance, field_name)
            current_value = getattr(to_instance, field_name)
            if field.editable and not field.auto_created and current_value != new_value:
                changed_fields.append(field_name)
                #print "%s: %s" % (field_name, str(new_value))
                setattr(to_instance, field_name, new_value)
        except models.FieldDoesNotExist:
            pass
    return changed_fields

def get_class_from_path(path):
    # Given a Python module path, this function returns the referenced class.
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

def render_message(template_name, context_dict, remove_newlines=False):
    """
    Shortcut method for rendering message templates, such as the ones used for
    activation emails.
    """
    message = get_template(template_name).render(Context(context_dict, autoescape=False))
    if remove_newlines:
        message = normalize_newlines(message).replace('\n', '')
    return message

def qualified_url(path, site, scheme='http'):
    """
    Returns a fully qualified URL (including domain and port) for a given path,
    which is necessary in contexts such as emails, when you need absolute links
    instead of relative, path-only links as returned by Django's ``reverse``
    method.
    """
    return '%(scheme)s://%(authority)s%(path)s' % {
        'scheme': scheme,
        'authority': site.domain,
        'path': path
    }
