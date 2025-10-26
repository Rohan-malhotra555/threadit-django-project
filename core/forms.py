from django.contrib.auth.forms import UserCreationForm
from django import forms    

"""
You have two classes because they do two different jobs:

SignUpForm (Outer): Defines the features (the bricks).

Meta (Inner): Defines the configuration (the instructions for how to use the bricks).
"""
class SignUpForm(UserCreationForm):

    # We are adding an email field and making it required.
    # The default Django sign-up form doesn't require an email.
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):

        # We are inheriting all the settings from the
        # original UserCreationForm's "Meta" class.
        
        # We just want to add our new 'email' field to the
        # list of fields that are displayed on the form.
        fields = UserCreationForm.Meta.fields + ('email',)

