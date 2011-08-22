Overview
********

django-user-profiles is a flexible app that wires together Django's user
authentication and user profile features, with customizable forms and models.
Furthermore, it provides a module for user profile activation, plus basic
support for a multiple-profiles-per-user feature.

This app also aims to offer some improvements where the standard
``django.contrib.auth`` app falls short.

Given the appropriate configuration, you can implement various login/signup
paradigms:

* Sign up with username and email / confirm email address / proceed to log in
  with generated password (NOT IMPLEMENTED)
* Sign up with email and password / confirm email address / proceed to log in
* Sign up with email and password / proceed to log in / confirm email address
  later to use advanced features
* Sign up with username and password / proceed to log in / add email address
  later / confirm email address.

.. note::
   This app builds upon Django's concept of `storing additional information
   about users
   <https://docs.djangoproject.com/en/1.3/topics/auth/#storing-additional-information-about-users>`_,
   so you should make sure to read all revelant Django documentation in order to
   properly use this app.
