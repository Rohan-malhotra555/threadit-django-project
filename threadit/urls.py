"""
URL configuration for threadit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# 1. You MUST import the 'include' function
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. Add this new path rule.
    # This tells Django: "For any URL that matches the pattern '' 
    # (which is the homepage), pass the request over to the 
    # file specified in 'core.urls' to be handled."
    path('', include('core.urls')),

]
