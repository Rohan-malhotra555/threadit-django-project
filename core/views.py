from django.shortcuts import render
from .models import Post

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



