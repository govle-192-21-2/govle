# govle

This is a course requirement for CS191/192 Software Engineering Courses of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman under the guidance of Ma. Rowena C. Solamo for AY 2020-2021.

Crisostomo, Coleen Anne F.

Dantis, Aurel Jared C.

Peroz, JC Mae M.

Sadang, Lee Monique C.

## About

GoVLê (Google + UVLê) is an integration hub for online learning platforms, initially created with support for aggregating data from both Google Classroom and Moodle. It is built using the Flask framework for the backend and the Bootstrap 4 framework for the frontend.

For the purposes of fulfilling the CS191/192 course requirements, it is currently hosted on Oracle Cloud and publicly accessible at [govle.dantis.me.](https://govle.dantis.me) At the time of writing, the project is considered incomplete, and user experience will not reflect the final design.

## Requirements

- Python 3.9.7
- `pip install -r requirements.txt` (don't forget to use a virtualenv)
- A working Firebase Realtime Database
  - Make sure to create and download service account credentials as `credentials.json` at the project root folder.
- A Google OAuth2 Client ID
  - Make sure to create and download client secrets as `client_secret.json` at the project root folder.
  - Don't forget to set up the OAuth2 consent screen in the Google Cloud console, using the necessary Google Classroom API permissions.

## Deployment

This project is built using Flask, so deployment for development purposes is as easy as 

```bash
FLASK_APP=app.py FLASK_ENV=development flask run
```

For production servers, however, it is strongly recommended that you use a proper WSGI server, and secure the server accordingly with SSL, as the web app deals with sensitive user data such as passwords.

If you're using uWSGI like we are, you can use the following command to deploy the app:

```bash
uwsgi --ini uwsgi.ini
```

This will make your app accessible at `http://127.0.0.1:29001`, which you can change in `uwsgi.ini`.