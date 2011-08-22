django-user-profiles
********************

A flexible app that wires together Django's user authentication and user profile
features, with customizable forms and models. Furthermore, it provides a layer
for user profile activation, plus support for a multiple-profiles-per-user
feature.

This app also aims to offer some improvements where the standard
`django.contrib.auth` app is too limited.

Given the appropriate configuration, you can implement various login/signup
paradigms:

* Sign up with username and email – confirm email address – proceed to log in
  with generated password (*not implemented*)
* Sign up with email and password – confirm email address – proceed to log in
* Sign up with email and password – proceed to log in – confirm email address
  later to use advanced features
* Sign up with username and password – proceed to log in – add email address
  later – confirm email address.
