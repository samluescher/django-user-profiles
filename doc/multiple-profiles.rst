Implementing a multiple-profiles-per-user feature
*************************************************

This application provides very basic support for implementing a web site where
one user can have several profiles (as in different sets of contact
information), with one being their default profile that is returned by Django's
``user.get_profile()`` method. This is achieved by filtering profile objects
by the ``is_default`` field. Please see the :ref:`user profile base model
<models>` for more information on this subject.

Currently, django-user-profiles comes without any views for creating,
displaying, updating or deleting additional profiles (although this might change
in the future). You are responsible for creating such views yourself.

These views can be pretty standard, following the basic CRUD concept as seen in
most Django applications. You can use the standard model form provided by
django-user-profiles, and of course you need to make sure that users can only
edit their own profiles.

.. warning::
   If you are implementing a multiple-profiles-per-user feature in your project,
   you should prevent users from deleting their default profile by checking
   first whether ``is_default`` is ``True``. When creating additonal profiles
   for a user, you also need to make sure that the ``is_default`` field is
   ``True`` for exactly one profile object so as not to create any ambiguities
   that lead to errors. 
