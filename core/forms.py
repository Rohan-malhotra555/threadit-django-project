from django.contrib.auth.forms import UserCreationForm
from django import forms    

from .models import Post, Comment, Community # importing Post to be used for the model in the Posting functionality
from django.contrib.auth.models import User

"""
You have two classes because they do two different jobs:

SignUpForm (Outer): Defines the features (the bricks).

Meta (Inner): Defines the configuration (the instructions for how to use the bricks).
"""

# UserCreationForm is a built-in Django form used to create new users.

# It already includes:
# username
# password1
# password2 (for confirmation)
# So instead of writing a form from scratch, 
# you can just extend UserCreationForm to customize it.

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

# ModelForm is a Django class that creates a form based on a database model.
# Instead of manually defining fields and validation, you can tell Django:

# The below one is the old PostForm (without bootstrap)
# class PostForm(forms.ModelForm):
#     """
#     This is the form for creating a new Post.
#     We use forms.ModelForm to automatically build a form
#     from our Post model.
#     """
#     class Meta:
#         # 'model' tells the ModelForm which model to use.
#         model = Post
        
#         # 'fields' tells the form which fields from the model
#         # to show to the user.
#         # We only want them to edit the title, content, and community.
#         # The 'author' and 'created_at' will be set automatically.
#         fields = ['title', 'content', 'community', 'image']

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

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write a comment...'
            }),
        }

        # We remove the label because the placeholder is enough
        labels = {'content': ''}


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
        


#################################################################

class PostForm(forms.ModelForm):

    class Meta:

        model = Post
        fields = ['community', 'title', 'content', 'image']

        widgets = {

            # This 'widgets' part adds Bootstrap classes to the inputs automatically!
            'community': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What is on your mind?'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),

        }


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

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Community Name (e.g. Gaming)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What is this community about?'}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'url-name (e.g. gaming)'}),
        }