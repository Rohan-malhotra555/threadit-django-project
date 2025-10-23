# Threadit: A Python/Django Reddit Clone

This is a full-stack content aggregation platform built with Python and Django. This project is my primary focus for mastering backend development and building a professional portfolio piece.

**Status:** Currently in development (Phase 1: Setup Complete).

---

## My Command Log & Developer Notes

This is my personal cheatsheet to track all the commands and concepts I've learned during this project.

### 1. Mac Environment Setup (One-Time Setup)

* **Install Homebrew (Mac package manager):**
    ```bash
    /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
    ```
    *Note: This is the "App Store" for developers. It also installs **Git**.*

* **Install VS Code (Code Editor):**
    *Note: Download from the official website, unzip, and drag the app to the `Applications` folder.*

* **Install 'code' command in PATH:**
    *Note: Open VS Code, press `Cmd+Shift+P`, type `Shell Command: Install 'code' command in PATH`, and hit Enter. This lets me open folders from the terminal with `code .`.*

### 2. Project Ignition (Date: Oct 22, 2025)

* **Create GitHub Repo:**
    *Note: Did this on GitHub.com. Made it **Public**, added a **README**, and a **Python .gitignore** template. The `.gitignore` tells Git to ignore files we don't need to save (like our `venv`).*

* **Clone Repo to Local Machine:**
    ```bash
    git clone [https://github.com/YourUsername/threadit-django-project.git](https://github.com/YourUsername/threadit-django-project.git)
    ```
    *Note: This downloads the project from GitHub to my computer.*

* **Open Project in VS Code:**
    ```bash
    cd threadit-django-project
    code .
    ```
    *Note: `cd` means "change directory" to get into the folder. `.` means "this current folder."*

### 3. Foundation Day: Django Setup (Date: Oct 23, 2025)

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

### 4. Creating Our First "App" (Date: Oct 23, 2025)

* **Create the 'core' app:**
    ```bash
    python3 manage.py startapp core
    ```
    *Note: This creates the `core` folder. A Django "app" is a "room" in our "project" (the house). The `core` app will handle posts, comments, etc.*

* **Register the app:**
    *Note: I must tell the "house" that the "room" exists. I opened `threadit/settings.py` and added `'core'` to the top of the `INSTALLED_APPS` list.*

### 5. Git & GitHub Workflow (My Save Process)

* **Stage all changes:**
    ```bash
    git add .
    ```
    *Note: "Puts all my new files and changes into a box" to be saved.*

* **Commit (Save) changes:**
    ```bash
VScode
    git commit -m "Your descriptive message here"
    ```
    *Note: Creates a permanent snapshot (a "save point") with a message describing what I did.*

* **Push changes to GitHub:**
    ```bash
    git push
    ```
    *Note: Uploads my saved commits from my computer to the cloud (GitHub.com).*

* **GitHub Token Fix (Troubleshooting):**
    *Note: If `git push` fails and asks for a password, I can't use my normal GitHub password.
    1.  Go to `GitHub.com` -> `Settings` -> `Developer settings` -> `Personal access tokens` -> `Tokens (classic)`.
    2.  Generate a new token with `repo` scope (permission).
    3.  Copy the `ghp_...` token.
    4.  Use this token as my password in the terminal.*
