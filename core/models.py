from django.db import models

# --- 1. ADD THIS IMPORT ---
# Import the built-in User model from Django's authentication system
from django.contrib.auth.models import User

# Create your models here.

# This is the model for our "Subreddit"
# models.Model turns your Python class into a Django database table with superpowers.
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

    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)

    # --- 2. ADD THIS NEW FIELD --- Adding this feature for the Posting functionality.
    # This links every Post to a User.
    # We use on_delete=models.CASCADE so that if a User is deleted,
    # all of their posts are deleted too.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # We use a ManyToManyField to link a Post to many Users (who upvoted).
    # related_name='post_upvotes' gives us a way to find all posts a user
    # has upvoted (e.g., user.post_upvotes.all()).
    # blank=True means a post can have zero upvotes.

    # Forward name: upvotes (the field name you wrote on the Post model).

    # Reverse name: post_upvotes (the related_name you specified, which gets attached to the User model).
    # post.upvotes.all() → “Who liked this post?”
    # user.post_upvotes.all() → “Which posts did this user like?”
    upvotes = models.ManyToManyField(User, related_name='post_upvotes', blank=True)

    # We do the same for downvotes.
    downvotes = models.ManyToManyField(User, related_name='post_downvotes', blank=True)

    # upload_to='post_images/': This tells Django where to save the images.
    #   It will save them to 'MEDIA_ROOT/post_images/'
    # blank=True, null=True: This makes the image optional.
    #   A user can create a post *without* uploading an image.
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)

    @property
    def score(self):

        return self.upvotes.count() - self.downvotes.count()

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


"""

To explain this from scratch, imagine you are running a **Library**.

A library has two things:

1. **The Bookshelves:** Where the physical books are kept.
2. **The Computer Catalog:** A list that tells you *where* the book is (e.g., "Row 5, Shelf B").

**Django works exactly the same way:**

1. **The Media Folder (Bookshelf):** This is where the actual image file (JPEGs/PNGs) sits on your hard drive.
2. **The Database (Catalog):** This only stores the **address** of the image (e.g., `/media/post_images/cat.jpg`).

Here is the step-by-step recipe to add image functionality to a Django project.

### Step 1: Tell Django where the "Bookshelf" is (Settings.py)

Before you can upload anything, you must tell Django where to put the files on your computer.

Open `settings.py` and add these two lines at the bottom:

```python
# MEDIA_ROOT: The actual folder on your laptop where files are saved.
# We join 'BASE_DIR' (project folder) with a new folder name 'media'.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_URL: The web address users type to see the image.
# http://127.0.0.1:8000/media/dog.jpg
MEDIA_URL = '/media/'

```

### Step 2: Create the "Catalog Entry" (Models.py)

Now you need a column in your database to remember the filename.

Open `models.py`:

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    # upload_to='post_images/' tells Django: 
    # "Inside the Media folder, make a sub-folder called post_images and put it there."
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

```

* *Note:* You usually need to install a library called Pillow for this to work (`pip install Pillow`), because Python doesn't know how to handle images by default.

### Step 3: The "Magic" URL (Urls.py) - *The Most Confusing Part*

This is the step everyone forgets. By default, Django **refuses** to show images from your hard drive for security reasons. You have to explicitly tell it to allow this during development.

Open `urls.py` (the main one):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your other paths ...
]

# This checks: "Are we in development mode (DEBUG=True)?" 
# If yes, "Add a special URL path that lets the browser look inside MEDIA_ROOT."
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

**Without this code, your image uploads, but the image will look "broken" on the website.**

### Step 4: The Delivery Truck (The HTML Form)

Now the frontend. Standard HTML forms are designed to send **text**, not heavy files. You have to upgrade the form.

Open your template (e.g., `create_post.html`):

```html
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>

```

### Step 5: The Receptionist (Views.py)

Finally, you catch the data in your view.

Open `views.py`:

```python
def create_post(request):
    if request.method == 'POST':
        # Request.POST contains the text (title).
        # Request.FILES contains the image.
        # YOU MUST INCLUDE BOTH!
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save() # Django automatically saves the file to the folder AND the path to the DB.

```

---

### Summary of the Flow

1. **User** selects `cat.jpg` and clicks Submit.
2. **Browser** sends the file because of `enctype`.
3. **View** receives `request.FILES`.
4. **Django** looks at `MEDIA_ROOT` and saves `cat.jpg` into your `media` folder.
5. **Django** looks at the Database and saves the text `"post_images/cat.jpg"` in the `image` column.
6. **Browser** requests the image later, and `urls.py` directs it to the right folder.

"""