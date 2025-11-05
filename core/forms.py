from django.contrib.auth.forms import UserCreationForm
from django import forms    

from .models import Post, Comment, Community # importing Post to be used for the model in the Posting functionality
from django.contrib.auth.models import User

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

`forms.ModelForm` is a **smart form builder** that automatically 
creates a complete form by reading the "blueprint" of your `Post` model. 
It generates all the correct fields, validation, and a `.save()` method 
based on your model's structure.
"""


# Creating a new form for the comment section.

class CommentForm(forms.ModelForm):
    """
    This is the form for adding a new Comment.
    """
    class Meta:
        # Tell the form which model to use
        model = Comment
        
        # Tell the form which fields to show.
        # We only want the user to type in the 'content'.
        # The 'author' and 'post' will be set automatically
        # in the view function.
        fields = ['content']


class CommunityForm(forms.ModelForm):

    """
    This is the form for creating a new Community.
    It's a ModelForm built from our Community model.
    """
    class Meta:

        # model = Community: Tells the ModelForm to use our
        # Community model as its blueprint.
        model = Community

        # fields = ['name', 'description']: Tells the form to
        # only show these two fields to the user.
        # 'created_at' is set automatically by the model.
        fields = ['name', 'description']


class EditProfileForm(forms.ModelForm):
    """
    This is the form for editing a user's profile.
    It's a ModelForm based on the built-in User model.
    """
    class Meta:
        # model = User: Tells the form to use the built-in
        # User model as its blueprint.
        model = User
        
        # fields = ['username', 'email']: Tells the form to
        # only show these two fields. We don't want users
        # editing their password from this form.
        fields = ['username', 'email']
        