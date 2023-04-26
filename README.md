# user-auth
# User Auth : Django

This is a Django project that can be implemented using Django REST framework. The feature 
is related to user registration and login and involves the use of OTP (One-Time Password) verification to ensure 
that only verified users can log in to the application.

# Setup

Important : Python3.10 should be used while working on this project.
The first thing to do is to clone the repository:

$ git clone https://github.com/shyamsharma-kiwi/user-auth.git
$ cd user-auth
Create a virtual environment to install dependencies in and activate it:

$ python3 -m venv venv
$ source venv/bin/activate
Then install the dependencies:

(venv)$ pip install -r requirements.txt
Note the (venv) in front of the prompt. This indicates that this terminal session operates in a virtual environment 
set.

Once pip has finished downloading the dependencies:
Setup database configurations in settings.py file as per your need. It will look like this if you use postgres:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your_database>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

Now run following commands:
(venv)$ python manage.py runserver
And navigate to http://127.0.0.1:8000/apidoc/ to open swagger to access APIs.
