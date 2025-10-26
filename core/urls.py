from django.urls import path
from . import views  # This means "from the same directory, import the views.py file"

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
]