from django.contrib import admin
from .models import Community, Post  # 1. Importing models
# Registering models here

# 2. Telling the admin site to manage the Community model
admin.site.register(Community)

# 3. Telling the admin site to manage the Post model
admin.site.register(Post)

