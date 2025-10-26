from django.shortcuts import render, redirect
from .models import Post

from django.contrib.auth import login
from .forms import SignUpForm # <-- Import our new form

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