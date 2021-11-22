# Clucker
> An example Django project - a microblogging twitter-like web app

This is a web app project used to learn the fundamentals of Django and Python. It was completed for KCL's "Software Engineering Group Project" module.

This web app is a copy of Twitter's basic features. It allows a user to sign up/login, create posts, view other users, follow other users, and see follower posts on a feed.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```
