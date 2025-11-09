# Threadit: A Full-Stack Content Platform 🚀

A full-stack content aggregation and discussion platform built from the ground up using Python and Django. This project allows users to create communities, submit image-based posts, vote, and comment on content. The entire application is deployed to a live production environment.

## 🚀 Live Demo

You can view the live, deployed application here:
**[https://rohan-threadit.onrender.com](https://rohan-threadit.onrender.com)**

---

## 📸 Project Screenshot


<img width="959" height="762" alt="image" src="https://github.com/user-attachments/assets/b54edb8e-28e2-44a8-ab79-20fd740fafa9" />



---

## ✨ Core Features

* **Full User Authentication:** Secure user sign-up, login, and logout functionality.
* **Community Creation:** Logged-in users can create and name their own communities.
* **Post Creation (with Images):** Users can create new posts with a title, content, an optional image upload, and assign them to a community.
* **Full CRUD Functionality:** Users have full Create, Read, Update, and Delete (CRUD) permissions on their *own* posts and comments.
* **Dynamic Feeds:**
    * **Homepage:** A paginated feed of all posts from all communities.
    * **Community Page:** A dynamic page for each community, showing only its posts.
    * **Profile Page:** A dynamic page for each user, showing their post and comment history.
* **Voting System:** A "Reddit-style" upvote/downvote system on all posts, with visual feedback to show what the user has voted.
* **Commenting System:** Users can add and delete comments on posts.
* **Protected Actions:** All core actions (posting, commenting, voting, editing) are protected by `@login_required` to ensure only authenticated users can participate.

---

## 💻 Tech Stack & Key Concepts

This project was built using a modern, production-ready stack:

* **Backend:**
    * **Python 3.9**
    * **Django 4.2**: The core backend framework.
    * **Gunicorn**: The production-ready web server (WSGI).

* **Frontend:**
    * **HTML5**
    * **CSS3** (with Flexbox for layout)
    * **Django Template Language (DTL)**: Used for dynamic rendering, template logic, and filters.

* **Database:**
    * **PostgreSQL** (hosted on **Neon**) for production.
    * **SQLite3** for local development.
    * **Django ORM**: Used for all database queries and relationship management (`ForeignKey`, `ManyToManyField`).
    * `dj-database-url`: For parsing database credentials in production.

* **Deployment & Storage:**
    * **Render**: The cloud platform (PaaS) hosting the live web service.
    * **Whitenoise**: For efficiently serving static CSS files in production.
    * **Cloudinary**: For external, persistent storage of user-uploaded media (images).

* **Developer Tools:**
    * **Git & GitHub**: For version control.
    * **Virtual Environments** (`venv`): For managing dependencies.

---

## 🔧 Running This Project Locally

To run this project on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Rohan-malhotra555/threadit-django-project.git](https://github.com/Rohan-malhotra555/threadit-django-project.git)
    cd threadit-django-project
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Database Migrations:**
    This will create your local `db.sqlite3` file and build all the tables.
    ```bash
    python3 manage.py migrate
    ```

5.  **Create a Superuser:**
    You'll need an admin account to test the admin panel.
    ```bash
    python3 manage.py createsuperuser
    ```

6.  **Run the Development Server:**
    ```bash
    python3 manage.py runserver
    ```
    The project will be available at **`http://127.0.0.1:8000/`**.

---

## 👤 Author

* **Rohan Malhotra**
    * [LinkedIn](www.linkedin.com/in/rohan-malhotra-0b6327251)
    * [GitHub](https://github.com/Rohan-malhotra555)

---

## 📄 License

This project is licensed under the MIT License.
