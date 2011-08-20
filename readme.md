Django User Profiles

A flexible app that wires together Django's user authentication and user profile
features, with customizable forms and models.

This app also provides a layer for user profile activation, plus abstract
support for a multiple-profiles-per-user feature.

Given the appropriate configuration, you can implement various login/signup
paradigms:

* Sign up with username and email – confirm email address – proceed to log in
  with generated password *NOT IMPLEMENTED*
* Sign up with email and password – confirm email address – proceed to log in
* Sign up with email and password – proceed to log in – confirm email address
  later to use advanced features
* Sign up with username and password – proceed to log in – add email address
  later – confirm email address.
