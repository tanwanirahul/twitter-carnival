twitter-carnival
================

A sample application for integration with Twitter and aggregating all the Tweets tagged #Carnival


How to use?
============
1. Install postgres SQL.
    * run the commands specified in postgres.install

2. Install the dependencies.
    * pip install -r requirements.txt

3. Collect the static content.
    * python manage.py collecstatic

4. Create the database.
    * python manage.py syncdb

5. Apply the migrations.
    * python manage.py migrate album
  
6. Get updates form twitter for #Carnival.
    * python manage.py search

7. Run tests.
    * python manage.py test

8. Run the application.
    * python manage.py runserver



Endpoints:
==============

1. / - For browsing the photos (Photo gallery)

2. /api/v1/tweets/ - REST API for getting the tweets tagged with #carnival.

3. /api/v1/media/  - REST API for the corresponding photos.

4. /api/v1/users/  - REST API for the associated users.



Get continous updates from twitter:
====================================

To get the updates from twitter, make a cron job to trigger *_python manage.py search command_ * on frequent basis.
