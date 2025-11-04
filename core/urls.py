from django.urls import path
from . import views  # This means "from the same directory, import the views.py file"
from django.contrib.auth import views as auth_views # Import Django's built-in authentication views


# This list holds all the URL patterns for just this one app
urlpatterns = [
    # This is our first URL pattern
    # path(URL_PATTERN, VIEW_FUNCTION, NICKNAME)
    
    # URL_PATTERN: ''
    # This matches the "root" path. So, if our app is at the homepage, this matches.
    
    # VIEW_FUNCTION: views.home
    # This is the actual Python function that will be called. We are pointing 
    # to the 'home' function inside our 'views.py' file.
    
    # NICKNAME: name='home'
    # This is a unique, human-readable name for this URL. It lets us
    # refer to this link easily in our HTML templates without hard-coding the URL.
    path('', views.home, name='home'),

    
    # Path for our new sign-up page
    #
    # 'signup/': This is the "address." It means when a user
    #             visits http://127.0.0.1:8000/signup/
    #             this rule will match.
    #
    # views.signup: This is the "brain." We are telling Django,
    #                "When this URL is visited, you must call the
    #                function named 'signup' inside our core/views.py file."
    #
    # name='signup': This is the "nickname." It gives this URL a
    #                unique name, so we can refer to it easily
    #                from our HTML templates (e.g., <a href="{% url 'signup' %}">Sign Up</a>).

    path('signup/', views.signup, name='signup'), 

    # Path for the login page
    # We use Django's built-in LoginView.
    # We need to tell it which template to use for the login form.
    # .as_view is used to convert the class LoginView to a callable function for the url pattern.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # Path for the logout action
    # We use Django's built-in LogoutView.
    # By default, it redirects to the LOGOUT_REDIRECT_URL setting (or admin page).
    # We don't need a template for logout itself, it's just an action.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Path for the community detail page (Dynamic URL)
    #
    # 'community/<str:community_name>/': This is the pattern.
    #   - 'community/': Matches the literal text "community/".
    #   - '<str:community_name>': This is the DYNAMIC part.
    #     - Angle brackets `< >` signal a variable part.
    #     - `str:` tells Django to expect a string (text).
    #     - `community_name`: This is the NAME we give to the variable
    #       that will capture whatever text is in this part of the URL
    #       (e.g., "python", "django").
    #   - '/': Matches the final slash.
    #
    # views.community_detail: This tells Django to call the function named
    #                         'community_detail' in our `views.py` file
    #                         when this pattern matches. (We'll create this next).
    #
    # name='community_detail': The unique nickname for this URL pattern.

    path('community/<str:community_name>/', views.community_detail, name='community_detail'),

# --- ADD THIS NEW LINE for the create new post functionality---

    # Path for the new "create post" page
    # This maps the URL '/create-post/' to a new view
    # we will create called 'create_post'.
    path('create-post/', views.create_post, name='create_post'),

    # Path for the Post Detail page
    # This is a dynamic URL. <int:post_id> is a "path converter".
    # It captures the number from the URL (e.g., '1', '2') as an
    # integer and passes it to the view as a variable named 'post_id'.
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

# Path for upvoting a post
    # This will be triggered when a user clicks an upvote link
    # e.g., /post/5/upvote/
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),

    # Path for downvoting a post
    # e.g., /post/5/downvote/
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),

    # Path for the User Profile page
    # This is a dynamic URL that captures a string (the username)
    # e.g., /user/rohan/
    path('user/<str:username>/', views.profile_view, name='profile'),

]