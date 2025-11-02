from django.shortcuts import render, redirect, get_object_or_404 # added get_object_or_404 for the specific community search.
from .models import Post, Community  # added Community for the specific community search

from django.contrib.auth import login
from .forms import SignUpForm, PostForm # <-- Import our new form

# This "decorator" is what we'll use to protect the view
from django.contrib.auth.decorators import login_required 




def home(request):

    # 1. Get all the Post objects from the database
    #    We use .order_by('-created_at') to show the newest posts first.
    posts = Post.objects.all().order_by('-created_at')

    # 2. Define the "context"
    #    This is a Python dictionary that passes our data to the template.
    #    The key ('posts') is the name we'll use in the HTML.
    context = {

        'posts': posts,
    }

    # 3. Render the HTML page (home.html) and send it back
    return render(request, 'core/home.html', context)


# The Signup class

def signup(request):
    """
    This view handles user registration.
    """
    # Check if the user is submitting the form (POST) or just visiting (GET)
    if request.method == 'POST':
        # This is a POST request. The user has submitted the form.
        # Create a form instance and fill it with the submitted data
        form = SignUpForm(request.POST)
        
        # Check if the form's data is valid (e.g., passwords match, email is valid)
        if form.is_valid():
            # The form is valid! Save the new user to the database.
            user = form.save()
            
            # Log the user in automatically after they sign up
            login(request, user)
            
            # Redirect them to the homepage ('home')
            return redirect('home')
    else:
        # This is a GET request. The user is just visiting the page.
        # Create a new, blank instance of our form
        form = SignUpForm()
    
    # Put the form into a context dictionary to pass to the template
    context = {
        'form': form,
    }
    
    # Render the signup.html template with the form
    return render(request, 'core/signup.html', context)


# Function for community specific search

def community_detail(request, community_name):
    
    """
    Shows details for a specific community and lists its posts.
    """
    # 1. Find the Community object based on the name from the URL.
    #    get_object_or_404 is a handy shortcut:
    #    - It tries to get the Community where the 'name' field matches community_name.
    #    - If it finds one, it returns the object.
    #    - If it finds *none*, it automatically raises a 404 "Page Not Found" error.
    # IMPORTANT: the community name is case sensitive.
    community = get_object_or_404(Community, name=community_name)

    # In order to search in a non case-sensitive way, use __iexact
    # community = get_object_or_404(Community, name__iexact=community_name)

    # 2. Get all posts that BELONG TO this specific community.
    #    We filter the Post objects where the 'community' field (our ForeignKey)
    #    is exactly the community object we just found.
    #    We also order them by creation date.
    posts = Post.objects.filter(community=community).order_by('-created_at')

    # 3. Create the context dictionary to pass data to the template.
    context = {
        'community': community, # Pass the specific community object
        'posts': posts,         # Pass the filtered list of posts
    }

    # 4. Render the new template (which we'll create next).
    return render(request, 'core/community_detail.html', context)


# ----------------------------------------------
# View for creating a new post
# ----------------------------------------------

# ADD THIS "DECORATOR"
# This is a wrapper that Django runs *before* our view.
# It checks if the user is logged in.
# If they are NOT, it will automatically redirect them to the
# login page (using the 'LOGIN_REDIRECT_URL' from settings.py).
@login_required 
def create_post(request):
    """
    Handles the creation of a new post.
    """
    # Check if the user is submitting the form (POST) or just visiting (GET)
    if request.method == 'POST':
        # This is a POST request. User is submitting the form.
        # Create a form instance and fill it with the submitted data
        form = PostForm(request.POST)
        
        # Check if the form's data is valid
        if form.is_valid():
            # The form is valid! But DON'T save to database just yet.
            # commit=False creates the object in memory but doesn't
            # save it. This lets us add the author first.

            """
            we already have the request.user in hand but how do we assign it to 
            the new_post, if the new_post is not created in the first place, so we 
            have to create it, stop it from saving finally and then apply modification 
            of adding the author and then save it finally.
            """
            new_post = form.save(commit=False)
            
            # --- THIS IS THE KEY ---
            # Set the 'author' field of the new post to be the
            # user who is currently logged in.
            # 'request.user' is the logged-in User object from the middleware.
            new_post.author = request.user
            
            # Now, save the completed object to the database.
            new_post.save()
            
            # Redirect the user back to the homepage
            return redirect('home')
    else:
        # This is a GET request. The user is just visiting the page.
        # Create a new, blank instance of our PostForm.
        form = PostForm()

    # Put the form (either blank or with errors) into context
    context = {
        'form': form,
    }
    
    # Render the 'create_post.html' template (we'll make this next)
    return render(request, 'core/create_post.html', context)



