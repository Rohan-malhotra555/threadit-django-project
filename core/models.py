from django.db import models

# --- 1. ADD THIS IMPORT ---
# Import the built-in User model from Django's authentication system
from django.contrib.auth.models import User

# Create your models here.

#This is the model for our "Subreddit"
class Community(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True) # blank=True means this field is optional
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the time when created

    def __str__(self):
        return self.name
    
# This is the model for our "Post"
class Post(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True) # A post can have a title but no text content (e.g., a link post)
    created_at = models.DateTimeField(auto_now_add=True)

    # This is the most important part!
    # It creates a many-to-one relationship.
    # One Community can have MANY Posts.
    # on_delete=models.CASCADE means: "If a Community is deleted, delete all its Posts too."

    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    # --- 2. ADD THIS NEW FIELD --- Adding this feature for the Posting functionality.
    # This links every Post to a User.
    # We use on_delete=models.CASCADE so that if a User is deleted,
    # all of their posts are deleted too.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
# Creating a new model for the comment functionality

class Comment(models.Model):
    # This is the actual text content of the comment.
    content = models.TextField()

    # This timestamp will be set automatically when the comment is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # This links the Comment to the User who wrote it.
    # If a User is deleted, all their comments are deleted too.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # This links the Comment to the Post it's replying to.
    # If a Post is deleted, all its comments are deleted too.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        # This will make the admin panel show the first 50 characters
        # of the comment, so it's easy to identify.
        # on the first 50 characters will be shown as the 'name'.
        return self.content[:50]
    


"""
User is a class that is there to maintain the information 
about the users information. It is used to retrieve information
and for this session id purposes.
it is the actual main table to store user information given by 
django itself, we don't create it.

now the User that we imported from ..auth.models import User,
this is the same user model that we are talking about in the
above line.

now, when we say post.author.username, it actually means post's 
author which is the link to the User model, now we want user's 
username so the chain follows up.
"""