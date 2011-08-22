.. _activation:

User Activation
***************

Many web applications require some form of user activation, usually to verify
user-provided information such as email addresses. django-user-profiles provides
an activation module, implemented as a Django application.


Installation
============

- In order to enable activation, add the ``activation`` module to your
  ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ... your other apps here 
        'user_profiles',
        'user_profiles.activation',
    )

- Include the activation URLconf in your ``urls.py``::

    urlpatterns = patterns('',
        # ... your urls here
        (r'^user/', include('user_profiles.activation.urls')),
    )

.. note::
   Whenever new user sign up, they will now be sent an activation request via
   email. However, if you want to prevent new users from logging in unless they
   have activated, you need to set :ref:`USER_PROFILES_USER_SET_ACTIVE_ON_SIGNUP
   <user-profiles-user-set-active-on-signup>` to ``False`` in your project's
   settings module. Sometimes you also need to re-request activation from users,
   for instance when they change their email address. See
   :ref:`activation-utility` for more information.

This application automatically connects to the ``post_signup`` signal dispatched
by django-user-profiles in order send to request activation from new users.
See the :ref:`signals documentation <user-profiles-signals>` for more
information.


.. _activation-templates:

Message templates
=================

For rendering the activation request email, text templates are used. You are
likely to require your own customized messages. To customize the email text,
simply your own templates with the following names: 

``activation/email/activation_request.subject.txt``
    The subject line of the activation email. 
    
``activation/email/activation_request.txt``
    The body text of the activation email. This should display the activation
    key to the user, plus a link to the activation page and form. Example template::
 
        Dear {{ recipient }}, please go to {{ url }} to activate your account.
        If the above link doesn't work, go to {{ form_url }} and enter the
        following key: {{ key }}
    

The following context variables are available to both of these templates:

``url``
    The activation link URL

``form_url``
    The link to the activation form

``site_url``
    The link to the website that requires activation

``site``
    The corresponding ``Site`` object

``key``
    The activation key

``user``
    The associated ``User`` object

``recipient``
    An object that resolves to a string containing the name of the user (i.e.
    either the user or the profile object, depending on whether the profile
    model has a ``__unicode__`` method).

``profile``
    The associated user profile object.

``created``
    If the user was just created, this will ``True``. If the user already
    existed, it will be ``False``. You are probably going to want to address
    users in a different way if the just signed up.


Views
=====

.. automodule:: user_profiles.activation.views
   :members:

.. _activation-utility:

Utility functions
=================

.. autofunction:: user_profiles.activation.utils.require_activation_from_user

.. autofunction:: user_profiles.activation.utils.accept_activation_code
