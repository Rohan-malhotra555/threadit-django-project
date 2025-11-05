from django.shortcuts import render, redirect, get_object_or_404 # added get_object_or_404 for the specific community search.
from .models import Post, Community, Comment  # added Community for the specific community search

from django.contrib.auth import login
from .forms import SignUpForm, PostForm, CommentForm, CommunityForm # <-- Import our new form

# This "decorator" is what we'll use to protect the view
from django.contrib.auth.decorators import login_required 

from django.contrib.auth.models import User # for the user profile page

from django.core.paginator import Paginator # for the creation of the pages in home page. 




def home(request):

    # 1. Get all the Post objects from the database
    #    We use .order_by('-created_at') to show the newest posts first.
    # posts = Post.objects.all().order_by('-created_at')

    # 2. Define the "context"
    #    This is a Python dictionary that passes our data to the template.
    #    The key ('posts') is the name we'll use in the HTML.
    # context = {

    #     'posts': posts,
    # }

    """
    This is the view for our homepage.
    It now includes pagination.
    """

    # 1. Get the list of ALL posts, in order (no change here).
    #    This is the "master list" we will paginate.
    post_list = Post.objects.all().order_by('-created_at')

    # 2. Create a Paginator object.
    #    We tell it:
    #    - What list to paginate (post_list)
    #    - How many items per page (e.g., 5)
    paginator = Paginator(post_list, 5)

    # 3. Get the page number from the URL's query parameters.
    #    e.g., /?page=1, /?page=2
    #    request.GET.get('page') looks for the 'page' parameter.
    page_number = request.GET.get('page')

    # 4. Get the "Page" object for the requested page number.
    #    paginator.get_page() is a safe way to do this.
    #    - If page_number is valid (e.g., 2), it gets Page 2.
    #    - If page_number is not provided (None), it gets Page 1.
    #    - If page_number is invalid (e.g., 999), it gets the last page. 
    page_obj = paginator.get_page(page_number)

    # 5. Define the "context".
    #    We no longer pass the *entire* list of posts.
    #    We pass the 'page_obj' which contains *only* the posts
    #    for the current page, plus all the pagination info.
    context = {

        'page_obj': page_obj,
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
    
    # """
    # Shows details for a specific community and lists its posts.
    # """
    # # 1. Find the Community object based on the name from the URL.
    # #    get_object_or_404 is a handy shortcut:
    # #    - It tries to get the Community where the 'name' field matches community_name.
    # #    - If it finds one, it returns the object.
    # #    - If it finds *none*, it automatically raises a 404 "Page Not Found" error.
    # # IMPORTANT: the community name is case sensitive.
    # community = get_object_or_404(Community, name=community_name)

    # # In order to search in a non case-sensitive way, use __iexact
    # # community = get_object_or_404(Community, name__iexact=community_name)

    # # 2. Get all posts that BELONG TO this specific community.
    # #    We filter the Post objects where the 'community' field (our ForeignKey)
    # #    is exactly the community object we just found.
    # #    We also order them by creation date.
    # posts = Post.objects.filter(community=community).order_by('-created_at')

    # # 3. Create the context dictionary to pass data to the template.
    # context = {
    #     'community': community, # Pass the specific community object
    #     'posts': posts,         # Pass the filtered list of posts
    # }

    # # 4. Render the new template (which we'll create next).
    # return render(request, 'core/community_detail.html', context)

    """
    Shows details for a specific community and lists its posts,
    now with pagination.
    """
    
    # 1. Get the Community object (no change)
    community = get_object_or_404(Community, name__iexact=community_name)
    
    # 2. Get the *complete* post list for this community (no change)
    post_list = Post.objects.filter(community=community).order_by('-created_at')
    
    # 3. Create a Paginator object for the posts
    paginator = Paginator(post_list, 5) # Show 5 posts per page

    # 4. Get the page number from the URL query parameter
    page_number = request.GET.get('page')

    # 5. Get the Page object for the posts
    page_obj = paginator.get_page(page_number)
    
    # 6. Package the context
    context = {
        'community': community,
        # Pass the 'Page' object, not the full list
        'page_obj': page_obj, 
    }
    
    # 7. Render the template (no change)
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



def post_detail(request, post_id):
    """
    Shows a single post, its comments, and handles new comment submissions.
    """
    # 1. Get the specific post object using the 'post_id' from the URL.
    #    If the post doesn't exist, this will show a 404 page.
    post = get_object_or_404(Post, id=post_id)
    
    # 2. Get all comments related to this *one* post.
    #    We filter the Comment model where the 'post' field
    #    matches our 'post' object. We order by the oldest first.
    comments = Comment.objects.filter(post=post).order_by('created_at')
    
    # 3. Create a blank instance of our comment form.
    #    This will be used to render the "Add a comment" box.
    comment_form = CommentForm()

    # 4. Handle the 'POST' request (when a user submits a comment)
    if request.method == 'POST':
        # This part will ONLY run if the user submits the form.
        # We fill the form instance with the submitted data.
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            # Form is valid. Create the comment object in memory.
            new_comment = comment_form.save(commit=False)
            
            # Assign the correct post and author (the logged-in user)
            new_comment.post = post
            new_comment.author = request.user
            
            # Now save the completed comment to the database.
            new_comment.save()
            
            # Redirect back to this *same page* (the post detail page).
            # This is a common pattern to show the new comment.
            return redirect('post_detail', post_id=post.id)
            
    # 5. Prepare the context dictionary for the template
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    # 6. Render the template
    return render(request, 'core/post_detail.html', context)


# The following code is for the VOTING SYSTEM functionality.

@login_required # Ensures only logged-in users can run this view
def upvote_post(request, post_id):
    """
    Handles upvoting a post.
    """
    # 1. Get the post object that the user is trying to upvote
    #    using the post_id from the URL.
    post = get_object_or_404(Post, id=post_id)
    
    # 2. Get the user object for the person making the request.
    user = request.user

    # 3. The Core Voting Logic
    
    # Case 1: Has the user already upvoted this post?
    if user in post.upvotes.all():
        # Yes. This means they are clicking "upvote" again to *remove* their upvote.
        post.upvotes.remove(user)
    
    # Case 2: Has the user already *downvoted* this post?
    elif user in post.downvotes.all():
        # Yes. This means they are changing their vote from down to up.
        # We must remove their downvote AND add their upvote.
        post.downvotes.remove(user)
        post.upvotes.add(user)
        
    # Case 3: The user has not voted on this post at all.
    else:
        # This is a new upvote. Add them to the upvotes list.
        post.upvotes.add(user)


    next_page = request.GET.get('next', 'home')
    
    """
    next_page = request.GET.get('next', 'home')

    request.GET: This is a dictionary-like object that holds all the query parameters from the URL.

    If your URL is .../upvote/?next=/post/1/, then request.GET is {'next': '/post/1/'}.

    If your URL is just .../upvote/ (with no ?), then request.GET is empty {}.

    .get('next', 'home'): This is a standard Python dictionary method.

    'next' (Argument 1): This is the key it tries to find in the request.GET dictionary.

    'home' (Argument 2): This is the default value to use if the key 'next' is not found.

    So, this one line means: "Look for a URL parameter named next. If you find 
    it, put its value (like /post/1/) into the next_page variable. If you don't 
    find it, put the string 'home' into the next_page variable instead."
    """
    return redirect(next_page)


@login_required # Ensures only logged-in users can run this view
def downvote_post(request, post_id):
    """
    Handles downvoting a post. This logic is the
    exact mirror opposite of the upvote_post view.
    """
    # 1. Get the post and user
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # 3. The Core Voting Logic (Reversed)

    # Case 1: Has the user already downvoted this post?
    if user in post.downvotes.all():
        # Yes. Remove their downvote.
        post.downvotes.remove(user)
    
    # Case 2: Has the user already *upvoted* this post?
    elif user in post.upvotes.all():
        # Yes. Change their vote from up to down.
        post.upvotes.remove(user)
        post.downvotes.add(user)
        
    # Case 3: The user has not voted on this post at all.
    else:
        # This is a new downvote. Add them to the downvotes list.
        post.downvotes.add(user)

    next_page = request.GET.get('next', 'home')
    
    # 4. Redirect back to the homepage.
    return redirect(next_page)

"""
You've perfectly traced the flow for the VOTING SYSTEM:

Click: User clicks the href="{% url 'upvote_post' post.id %}" link.

URL Route: core/urls.py matches the path and calls the upvote_post view.

View Logic: The upvote_post view runs. It gets the post and user, and then 
modifies the post.upvotes or post.downvotes list (e.g., post.upvotes.add(user)). This change is saved to the database immediately.

Redirect: The view finishes and sends a return redirect('home') command back 
to the browser.

New Request: The browser, following the redirect, makes a brand new GET 
request to the homepage (/).

Home View: The home view runs again, fetching the (now updated) posts from 
the database.

Template Render: The home.html template is rendered. When it gets 
to {{ post.score }}, it calls the score property, which runs the 
self.upvotes.count() - self.downvotes.count() calculation using the newly 
updated lists, displaying the correct score.
"""



def profile_view(request, username):
    # """
    # Shows a user's profile page, including their posts and comments.
    # """
    
    # # 1. Get the User object.
    # # We use get_object_or_404 to find one User where their 'username'
    # # field exactly matches the 'username' captured from the URL.
    # # If no user is found, it automatically shows a 404 Page Not Found.
    # profile_user = get_object_or_404(User, username=username)
    
    # # 2. Get all posts made by this user, newest first.
    # # We filter the Post model, looking for all posts where the
    # # 'author' field (our ForeignKey) is equal to the 'profile_user' object.
    # posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    # # 3. Get all comments made by this user, newest first.
    # # We do the same thing for comments, filtering by the 'author' field.
    # comments = Comment.objects.filter(author=profile_user).order_by('-created_at')
    
    # # 4. Package all our data into a context dictionary.
    # # Note: We use 'profile_user' to distinguish this from 'user',
    # # which is the default variable for the *logged-in* user.
    # context = {
    #     'profile_user': profile_user,  # The user whose profile we are viewing
    #     'posts': posts,                # The list of their posts
    #     'comments': comments,          # The list of their comments
    # }
    
    # # 5. Render the new template (which we'll create next).
    # return render(request, 'core/profile.html', context)

    # new paginator part

    """
    Shows a user's profile page, now with pagination for posts.
    """
    
    # 1. Get the User object (no change)
    profile_user = get_object_or_404(User, username=username)
    
    # 2. Get the user's *complete* post list (no change)
    post_list = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    # 3. Create a Paginator object for the posts
    paginator = Paginator(post_list, 5) # Show 5 posts per page

    # 4. Get the page number from the URL query parameter
    page_number = request.GET.get('page')

    # 5. Get the Page object for the posts
    posts_page_obj = paginator.get_page(page_number)
    
    # 6. Get all comments (we won't paginate these for now)
    comments = Comment.objects.filter(author=profile_user).order_by('-created_at')
    
    # 7. Package the context
    context = {
        'profile_user': profile_user,
        # Pass the 'Page' object, not the full list
        'posts_page_obj': posts_page_obj, 
        'comments': comments,
    }
    
    # 8. Render the template (no change)
    return render(request, 'core/profile.html', context)


@login_required # Ensures only logged-in users can run this view
def create_community(request):
    """
    Handles the creation of a new Community.
    """
    # Check if the user is submitting the form (POST) or just visiting (GET)
    if request.method == 'POST':
        # This is a POST request. User is submitting the form.
        # Create a form instance and fill it with the submitted data.
        form = CommunityForm(request.POST)
        
        # Check if the form's data is valid (e.g., name is not blank)
        if form.is_valid():
            # The form is valid! Save the new community to the database.
            # We save it to a variable to get the new object.
            new_community = form.save()
            
            # --- THIS IS THE BEST PRACTICE REDIRECT ---
            # Redirect the user to the detail page for the community
            # they just created.
            return redirect('community_detail', community_name=new_community.name)
    else:
        # This is a GET request. The user is just visiting the page.
        # Create a new, blank instance of our CommunityForm.
        form = CommunityForm()

    # Put the form (either blank or with errors) into context
    context = {
        'form': form, # Use 'form' to be consistent with our other templates
    }
    
    # Render the 'create_community.html' template (we'll make this next)
    return render(request, 'core/create_community.html', context)


@login_required # User must be logged in
def edit_post(request, post_id):
    """
    Handles editing an existing post.
    """
    # 1. Get the specific post object we want to edit
    post = get_object_or_404(Post, id=post_id)
    
    # 2. --- CRITICAL SECURITY CHECK ---
    #    Check if the currently logged-in user is the author of this post.
    if request.user != post.author:
        # If they are not the author, redirect them home.
        # (A real app might show a "403 Forbidden" error instead)
        return redirect('home')

    # 3. Check if the user is submitting the form (POST) or just visiting (GET)
    if request.method == 'POST':
        # This is a POST request. User is submitting the edited form.
        # We fill the PostForm with the new data from request.POST
        # AND we link it to the existing 'post' object using 'instance=post'.
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            # The form is valid! Save the changes to the *existing* post.
            form.save()
            
            # Redirect back to the post's detail page
            return redirect('post_detail', post_id=post.id)
    else:
        # This is a GET request. The user is visiting the edit page.
        # We create a PostForm and pre-fill it with the *existing*
        # data from the 'post' object by passing 'instance=post'.
        form = PostForm(instance=post)
    
    # 4. Prepare the context
    context = {
        'form': form,
        'post': post, # Pass the post object for the template to use
    }
    
    # 5. Render the template. We can REUSE our 'create_post.html'
    #    template for this, as it just shows a form.
    return render(request, 'core/create_post.html', context)


# --- ADD THIS NEW FUNCTION FOR DELETING ---

@login_required
def delete_post(request, post_id):
    """
    Handles deleting an existing post.
    """
    # 1. Get the specific post object
    post = get_object_or_404(Post, id=post_id)
    
    # 2. --- CRITICAL SECURITY CHECK ---
    if request.user != post.author:
        # If not the author, do nothing and redirect home
        return redirect('home')
    
    # 3. We only allow deletion via a POST request for security.
    #    (This prevents Google from accidentally deleting posts)
    if request.method == 'POST':
        # The user has confirmed the deletion. Delete the post.
        post.delete()
        
        # Redirect back to the homepage
        return redirect('home')
    
    # 4. If it's a GET request, we can show a confirmation page.
    #    (For simplicity, we'll just handle the POST)
    #    We can build a 'delete_confirm.html' template later.
    #    For now, we'll just redirect home if it's a GET.
    return redirect('post_detail', post_id=post.id)


@login_required
def edit_comment(request, comment_id):
    """
    Handles editing an existing comment.
    """
    # 1. Get the specific comment object
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 2. Security Check: Is the logged-in user the author?
    if request.user != comment.author:
        return redirect('home') # Or some other "forbidden" page

    # 3. Handle the GET vs. POST
    if request.method == 'POST':
        # User is submitting the form.
        # We bind the new data to the *existing* comment instance.
        form = CommentForm(request.POST, instance=comment)
        
        if form.is_valid():
            form.save()
            
            # --- FIX 1 (Redirect) ---
            # Redirect back to the post detail page that this
            # comment belongs to.
            return redirect('post_detail', post_id=comment.post.id)
    else:
        # User is visiting the page.
        # Show the form, pre-filled with the existing comment's data.
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment, # Pass the comment for the template
    }
    
    # We will need to create this new template
    return render(request, 'core/edit_comment.html', context)


@login_required
def delete_comment(request, comment_id):
    """
    Handles deleting an existing comment.
    """
    # --- FIX 2 (Variable Name) ---
    # Get the comment by 'comment_id' from the URL, not 'comment'
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 2. Security Check
    if request.user != comment.author:
        return redirect('home')
    
    # 3. Handle POST request (for security)
    if request.method == 'POST':
        # Store the post_id *before* we delete the comment
        post_id = comment.post.id
        
        # Delete the comment from the database
        comment.delete()
        
        # --- FIX 3 (Redirect) ---
        # Redirect back to the post detail page
        return redirect('post_detail', post_id=post_id)
    
    # 4. Handle GET request (if user just visits the URL)
    #    Just send them back to the post page.
    # --- FIX 4 (Redirect) ---
    return redirect('post_detail', post_id=comment.post.id)


