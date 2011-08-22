Installing django-user-profiles
*******************************

.. note::
   Please refer to the Django documentation on `storing additional information
   about users
   <https://docs.djangoproject.com/en/1.3/topics/auth/#storing-additional-information-about-users>`_
   for more information about how Django handles user profiles.

- Create a user profile model subclassing
  ``user_profiles.models.UserProfileBase``, and define it in your project
  settings (see :ref:`models`)::

    AUTH_PROFILE_MODULE = 'my_app.MyUserProfile'
   
- Add the ``user_profiles`` module to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ... your other apps here 
        'user_profiles',
    )

- Add ``user_profiles.middleware.CurrentUserMiddleware`` to your ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        # ... your other middleware classes here 
        'user_profiles.middleware.CurrentUserMiddleware',
    )


- Include the URLconf in your ``urls.py``::

    urlpatterns = patterns('',
        # ... your urls here
        (r'^user/', include('user_profiles.urls')),
    )

- If you want to enable user activation, you also need to install that module.
  See :ref:`activation`. 

