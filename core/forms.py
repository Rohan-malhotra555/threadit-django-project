from django.contrib.auth.forms import UserCreationForm
from django import forms    

from .models import Post # importing Post to be used for the model in the Posting functionality

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


# --- 2. ADD THIS NEW CLASS --- this comes under the content posting functionality.

class PostForm(forms.ModelForm):
    """
    This is the form for creating a new Post.
    We use forms.ModelForm to automatically build a form
    from our Post model.
    """
    class Meta:
        # 'model' tells the ModelForm which model to use.
        model = Post
        
        # 'fields' tells the form which fields from the model
        # to show to the user.
        # We only want them to edit the title, content, and community.
        # The 'author' and 'created_at' will be set automatically.
        fields = ['title', 'content', 'community']

"""
Here's a refined version of that line:

`forms.ModelForm` is a **smart form builder** that automatically 
creates a complete form by reading the "blueprint" of your `Post` model. 
It generates all the correct fields, validation, and a `.save()` method 
based on your model's structure.
"""

