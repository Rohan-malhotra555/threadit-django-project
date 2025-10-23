from django.db import models

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
    create_at = models.DateTimeField(auto_now_add=True)

    # This is the most important part!
    # It creates a many-to-one relationship.
    # One Community can have MANY Posts.
    # on_delete=models.CASCADE means: "If a Community is deleted, delete all its Posts too."

    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title