# UnicornAttractor Issue Tracker

## By Heather Olcot

### A web application built using Python with Django.

Uses django_crispy_forms for form css. 
Uses Pillow for image handling.
Uses S3 for image storage.

## Not matching brief:
The idea is that new features are quoted based on how long they will take and so an upper limit is given. Voting is available to all users but only one vote is allowed each. However commenting is only available to those who have contributed towards the project, and developers.

## Left to implement
Links to next and previous articles in the latest news blog

Refactor so that the commenting and updates are done together for devs? But not for users as users can't update. Would it be possible?


contact form python snippet from https://wsvincent.com/django-contact-form/


## Issues
How to filter on search results? As 'query' not carried through.

## Deployment
Users would need to add their email address into the sendMail function in contacts/views.py.