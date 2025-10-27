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
    #                (We haven't created this function yet, but we will in the next step!)
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

]