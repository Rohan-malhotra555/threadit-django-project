
# Threadit: A Python/Django Content Platform

This is a full-stack content aggregation and discussion platform built with Python and Django. This project is my primary focus for mastering backend development and building a professional portfolio piece.

**Status:** Currently in development (Building core features).

-----

## My Command Log & Developer Notes

This is my personal cheatsheet to track all the commands and concepts I've learned during this project.

### 1\. Mac Environment Setup (One-Time Setup)

  * **Install Homebrew (Mac package manager):**

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    *Note: This is the "App Store" for developers. It also installs **Git**.*

  * **Install VS Code (Code Editor):**
    *Note: Download from the official website, unzip, and drag the app to the `Applications` folder.*

  * **Install 'code' command in PATH:**
    *Note: Open VS Code, press `Cmd+Shift+P`, type `Shell Command: Install 'code' command in PATH`, and hit Enter. This lets me open folders from the terminal with `code .`.*

### 2\. Project Ignition (Date: Oct 22, 2025)

  * **Create GitHub Repo:**
    *Note: Did this on GitHub.com. Made it **Public**, added a **README**, and a **Python .gitignore** template. The `.gitignore` tells Git to ignore files we don't need to save (like our `venv`).*

  * **Clone Repo to Local Machine:**

    ```bash
    git clone https://github.com/YourUsername/threadit-django-project.git
    ```

    *Note: This downloads the project from GitHub to my computer.*

  * **Open Project in VS Code:**

    ```bash
    cd threadit-django-project
    code .
    ```

    *Note: `cd` means "change directory" to get into the folder. `.` means "this current folder."*

### 3\. Foundation Day: Django Setup (Date: Oct 23, 2025)

  * **Create Virtual Environment:**

    ```bash
    python3 -m venv venv
    ```

    *Note: Creates an isolated "bubble" or "toolbox" named `venv` for this project. This folder is ignored by Git because of our `.gitignore`.*

  * **Activate Virtual Environment:**

    ```bash
    source venv/bin/activate
    ```

    *Note: "Opens the toolbox." My terminal prompt MUST show `(venv)` at the beginning before I do anything else.*

  * **Install Django:**

    ```bash
    pip3 install django
    ```

    *Note: `pip3` is Python's package manager. This installs Django *inside* the active `(venv)` bubble.*

  * **Create Django Project Files:**

    ```bash
    django-admin startproject threadit .
    ```

    *Note: `django-admin` is the main "factory builder" command. `threadit` is the name of the main configuration folder. The `.` at the end is **crucial**—it prevents creating a messy extra folder.*

  * **Create Initial Database:**

    ```bash
    python3 manage.py migrate
    ```

    *Note: `manage.py` is our new "project control panel." `migrate` looks at all our apps and builds the database tables. This created the `db.sqlite3` file.*

  * **Run the Development Server:**

    ```bash
    python3 manage.py runserver
    ```

    *Note: Starts the server. I can see my site live at `http://127.0.0.1:8000/`. I stop the server with `Ctrl+C`.*

### 4\. Creating Our First "App" (Date: Oct 23, 2025)

  * **Create the 'core' app:**

    ```bash
    python3 manage.py startapp core
    ```

    *Note: This creates the `core` folder. A Django "app" is a "room" in our "project" (the house). The `core` app will handle posts, comments, etc.*

  * **Register the app:**
    *Note: I must tell the "house" that the "room" exists. I opened `threadit/settings.py` and added `'core'` to the top of the `INSTALLED_APPS` list.*

### 5\. Database Models (The Blueprint)

  * **Action:** Edited the `core/models.py` file.
  * **Concept:** Created Python classes (`Community`, `Post`) that inherit from `models.Model`. This inheritance gives them database "superpowers" (like `.save()`, `.objects.all()`).
  * **`ForeignKey` (Key Concept):** `community = models.ForeignKey(Community, on_delete=models.CASCADE)`
    *Note: This is the **most important** line. It creates a **many-to-one link**. One `Community` can have MANY `Posts`, but one `Post` can only belong to ONE `Community`. `on_delete=models.CASCADE` means if I delete a Community, all its Posts are deleted too.*
  * **`__str__(self)`:**
    *Note: Added `def __str__(self): return self.name`. This gives the object a human-readable name (like "python") which is used in the Admin panel, instead of the default "\<Community object (1)\>".*

### 6\. Migrations (Applying the Blueprint)

  * **Step 1: Make the Blueprint:**
    ```bash
    python3 manage.py makemigrations
    ```
    *Note: Django reads my `core/models.py` and generates a "blueprint" file (e.g., `core/migrations/0001_initial.py`) describing the new database tables.*
  * **Step 2: Build from the Blueprint:**
    ```bash
    python3 manage.py migrate
    ```
    *Note: Django reads the new blueprint file and runs the actual SQL commands to create the `core_community` and `core_post` tables in my `db.sqlite3` database.*
  * **Troubleshooting (My Mistake):**
    \*Note: I got an `OperationalError: no such column: core_post.created_at`. This was because I first had a typo (`create_at`) and then fixed it in `models.py`, but my *database* still had the old, bad column name.
      * **The Fix:** I had to run `makemigrations` and `migrate` *again* to apply the fix to the database.\*

### 7\. The Admin Panel (Our "Back Office")

  * **Create Admin User:**
    ```bash
    python3 manage.py createsuperuser
    ```
    *Note: Created my admin account. The password is hidden while typing.*
  * **Register Models:**
    *Note: Edited `core/admin.py`. I imported my models (`from .models import Community, Post`) and then registered them with `admin.site.register(Community)` and `admin.site.register(Post)`.*
  * **Test:**
    *Note: Logged into `http://127.0.0.1:8000/admin/` and successfully created my first `Community` and `Post` objects. This confirmed the database was working.*

### 8\. The Homepage (First MVT Workflow: Model-View-Template)

  * **Goal:** Show all posts on the homepage (`/`).
  * **Step 1: The View (`core/views.py`) - The "Brain"**
    \*Note: Created the `home(request)` function.
      * `posts = Post.objects.all().order_by('-created_at')` - Fetches all posts, newest first.
      * `context = {'posts': posts}` - Packages the data to send to the template.
      * `return render(request, 'core/home.html', context)` - Combines data and HTML.\*
  * **Step 2: The Template (`core/templates/core/home.html`) - The "Face"**
      * **Folder Structure (Key Concept):** Created `core/templates/core/`. This "namespacing" is crucial so Django can find the right `home.html` file.
      * **Template Tags (Key Concept):**
          * `{% ... %}` tags are for **logic** (e.g., `{% for post in posts %}`...`{% endfor %}`).
          * `{{ ... }}` tags are for **printing** data (e.g., `{{ post.title }}`).
          * `{{ post.created_at|date:"F d, Y" }}` - Used a **filter** (`|date`) to format the time.
      * **Troubleshooting (My Mistake):** Got `TemplateSyntaxError`. This was because Django tries to read comments\!
      * **The Fix:** Changed all my HTML comments \`\` to Django comments `{# ... #}`. (Alternatively, I could have removed any \`{ %\` characters from inside the HTML comments).
  * **Step 3: The URLs (`threadit/urls.py` & `core/urls.py`) - The "Map"**
      * **Project URLs (`threadit/urls.py`):** Added `path('', include('core.urls'))`. This tells the main project to check the `core` app's URL file for any matching path.
      * **App URLs (`core/urls.py`):** Created this new file. Added `path('', views.home, name='home')`. This maps the root URL (`''`) to our `home` view.
      * **`name='home'` (Key Concept):** This is a nickname. It lets us use `{% url 'home' %}` in our templates, which is safer than hard-coding the URL `/`.

### 9\. User Authentication (Signup, Login, Logout)

  * **Signup (Function-Based View):**

      * **URL:** Added `path('signup/', views.signup, name='signup')` to `core/urls.py`.
      * **Form (`core/forms.py`):** Created this new file. Made `SignUpForm` by inheriting from `UserCreationForm` (gives free password hashing/security).
      * **`class Meta` (Key Concept):** This inner class is the "configuration". We used `fields = UserCreationForm.Meta.fields + ('email',)` to add the `email` field to the default form.
      * **View (`core/views.py`):** Created `signup(request)`. Used `if request.method == 'POST':` to handle both showing the blank form (`GET`) and processing the submitted form (`POST`).
      * **Template (`core/templates/core/signup.html`):**
          * `method="POST"`: This attribute on the `<form>` tag is what triggers the `POST` logic in the view.
          * **`{% csrf_token %}` (Key Concept):** Mandatory security tag. Prevents **CSRF attacks** by adding a secret token to the form. Django checks this token on submission.
          * **`{{ form.as_p }}` (Key Concept):** Automatically renders the entire form (Username, Email, Passwords) wrapped in `<p>` tags. Also shows validation errors.
          * **`type="submit"` (Key Concept):** The `<button>` attribute that tells the browser to submit the parent `<form>`.

  * **Login / Logout (Class-Based Views):**

      * **URLs (`core/urls.py`):**
          * `from django.contrib.auth import views as auth_views` - Imported Django's built-in views.
          * `path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login')`
          * `path('logout/', auth_views.LogoutView.as_view(), name='logout')`
      * **`as_view()` (Key Concept):** `LoginView` is a *Class* (a blueprint). `.as_view()` is the method that turns it into a *function* that the URL router can use.
      * **Template (`core/templates/core/login.html`):** `LoginView` *automatically* provides the `form` variable to this template. We just had to render `{{ form.as_p }}`.
      * **Settings (`threadit/settings.py`):** Added `LOGIN_REDIRECT_URL = 'home'` and `LOGOUT_REDIRECT_URL = 'home'` to the bottom, so users go to the homepage after logging in or out.
      * **Homepage Update (`home.html`):** Added `{% if user.is_authenticated %}`...`{% else %}`...`{% endif %}` to show different links (Login/Signup vs. Hello, username/Logout).
      * **`user` variable (Key Concept):** The `user` object is *automatically* available in all templates (from middleware). `user.is_authenticated` is just a `True`/`False` flag on that object.

### 10\. Git & GitHub Workflow (My Save Process)

  * **Stage all changes:**

    ```bash
    git add .
    ```

    *Note: "Puts all my new files and changes into a box" to be saved.*

  * **Commit (Save) changes:**

    ```bash
    git commit -m "Your descriptive message here"
    ```

    *Note: Creates a permanent snapshot (a "save point") with a message describing what I did.*

  * **Push changes to GitHub:**

    ```bash
    git push
    ```

    *Note: Uploads my saved commits from my computer to the cloud (GitHub.com).*

  * **GitHub Token Fix (Troubleshooting):**
    \*Note: If `git push` fails and asks for a password, I can't use my normal GitHub password.

    1.  Go to `GitHub.com` -\> `Settings` -\> `Developer settings` -\> `Personal access tokens` -\> `Tokens (classic)`.
    2.  Generate a new token with `repo` scope (permission).
    3.  Copy the `ghp_...` token.
    4.  Use this token as my password in the terminal.\*

  * **Merge Conflicts (My Mistake):**
    *Note: Got `[rejected] (fetch first)` and `(non-fast-forward)` errors. This happened because I made a change on GitHub.com (`README.md`) that my local machine didn't have. My local branch and the remote branch had "diverged".*

  * **The Golden Rule:**
    \*Note: Always **Commit -\> Pull -\> Push**.

    1.  **Commit** your local work first (`git commit ...`).
    2.  **Pull** from the remote to merge any new changes (`git pull origin main`).
    3.  **Fix Conflicts** (if any). If Git opens the Vim editor for a merge message, just type `:wq` and press Enter to save and quit.
    4.  **Push** your merged work (`git push origin main`).\*
