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