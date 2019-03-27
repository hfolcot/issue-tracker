[![Build Status](https://travis-ci.org/hfolcot/issue-tracker.svg?branch=master)](https://travis-ci.org/hfolcot/issue-tracker)

# UnicornAttractor Issue Tracker
Demonstration application deployed [here](https://issue-tracker-hev.herokuapp.com/)

## By Heather Olcot

### A web application built using Python with Django.

---

An application to assist support for developers and users. End users of the application being supported can raise bugs in the app, suggest new features and contribute towards these. Developers can manage the bugs and features raised, dealing with them individually.

The demonstrated version of the app focuses on support of the fictional 'UnicornAttractor' application.


## Notes for CI assessors

### Possible issues
The contact form is working, however there is occassionally a 500 error caused when trying to test it. This is caused by Google blocking the attempted sign in and NOT a bug in the app.

### Not matching brief:
The idea is that new features are quoted based on how long they will take and so a finite cost is given. Voting is available to all users but only one vote is allowed each. However commenting is only available to those who have contributed towards the project, and developers.

## UX
---
The application can be used by most companies to support their own existing software, allowing users to report issues and suggest new features, and developers to communicate with the customer what stage the resolution/implementation has reached.

Planning documentation: 
[Planning.pdf](https://github.com/hfolcot/issue-tracker/blob/master/design/planning/Planning.pdf)
[Wireframes](https://github.com/hfolcot/issue-tracker/tree/master/design/Wireframes)

User stories:
•	As a user of the UnicornAttractor app, I would like to be able to suggest new features for the app, in order to have it fulfil my requirements more fully.
•	As a developer of the UnicornAttractor app, I would like to have a central location for all work remaining on the app, as well as a method for users to pay for the work, in order to keep the app up to date and generate income from it.


## Features
---
### Existing Features

*Full user authentication*
All users of the application can create a secure account with a username and password, to use for adding and viewing tickets. Developers can be given staff status by the administrator for the ability to update tickets. Users can view their own tickets in a personal dashboard and update their profile.

*Home page to view all tickets*
Users can view both features and bugs in separate tabs, and filter these by status. Results can also be sorted by different headings.

*Search function*
USers can perform a search to find tickets containing their selected keyword.

*Bug reporting*
End users can report bugs and follow the progress of these right through to a fix being implemented. A screenshot can be added to the title and description for extra clarity. Comments can be added by both users and developers so that full communication between each can be achieved.
Developers can update further details on each bug including status, priority and to whom it is assigned.
A voting application has been built which can create one vote per user, per ticket. Once a user has voted, they cannot vote on that ticket again.

*New feature suggestions*
End users can also suggest new features for the supported app. These are then assessed by the developers and a quote given for the cost of developing this new feature. End users can contribute towards this quoted target, and once it is reached the developers can work towards implementation. 

*Comments*
The comments function is a separate app within the Django setup, which is used for both tickets and news articles.

*Statistics*
The Django Rest Framework has been utilised along with charts.js in order to create a visual representation of the work done.

*News blog*
A blog has been included so that developers of the company can keep end users informed of the latest developments.

*Contact page*
A separate contact page has been added for users to get in touch with developers about anything that is not a bug/feature. (_Please note that in the demonstration version, this function may occassionally give a 500 error, this is due to an issue with the Gmail address being used - Google has been rejecting the login - rather than an error in the application._)

### Features left to Implement
As the application currently works, when sorting bugs by priority, it is done alphabetically. A future version of the app will number the priority choices so that when bugs are sorted this way, the order will be Critical, High, Medium, Low and vice versa.

Links to the next and previous articles would be a welcome addition in the blog.

A 'rejected' status would be useful for features.

## Technologies Used
---
The project was written in [Python](https://www.python.org/) using the [Django](https://www.djangoproject.com/) framework for routing, page rendering, authentication and security.

[heroku](https://www.heroku.com) - The demonstration of the project has been deployed on the heroku platform.

[Stripe](https://stripe.com/gb) - Stripe is used for the secure payments within the app.

Pages are written in [HTML](https://www.w3.org/html/) using [CSS3](https://www.w3.org/Style/CSS/Overview.en.html) for styling and [JavaScript](https://www.javascript.com/) with [JQuery](https://jquery.com/) for the Stripe functionality and some functions to enhance user experience. 

[ChartsJS](https://www.chartjs.org) has been used for the bar graphs in Statistics.

The [Django Rest Framework](https://www.django-rest-framework.org/) was used to set up an API for the statistics to query the data.

[Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) have been used for good CSS on all forms.

[Django Storages](https://django-storages.readthedocs.io/en/latest/) handles the AWS data storage functionality.

[Pillow](https://pillow.readthedocs.io/en/stable/) handles images.

The contact form uses the Django SendMail function. (Thanks to [this site](https://wsvincent.com/django-contact-form/))

## Testing 

There have been a number of automated tests written using Django TestCase. These are contained within each app and begin with 'test_*'.

Manual test documentation can be found [here](https://github.com/hfolcot/issue-tracker/tree/master/manual_tests).

Jasmine testing has been written for JavaScript functions.
To use, these scripts must be added to the base.html header above the local scripts: `
    <!-- Jasmine Testing -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasmine/3.1.0/jasmine.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasmine/3.1.0/jasmine-html.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasmine/3.1.0/boot.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jasmine/3.1.0/jasmine.css" />`
In addition, this needs to be added to the block bodyjs section of statistics.html:
`<script src="{% static 'js/spec.js' %}"></script>`


HTML Validator:
Error: Element ul not allowed as child of element small in this context. -- Contained within some of the Django forms which are rendered automatically.
All other HTML is now passing.

JSHint:
All JavaScript is now passing JS validator.

CSS Validator:
All code passed.

## Deployment

To deploy the application the following steps must be taken:

1. Create a new application within Heroku. See [Heroku docs](https://devcenter.heroku.com/)
2. Download the file from github as a zip file, and extract to your own environment.
3. Initialize a git repository, commit and push all folders to github.
4. Within the Deploy settings on Heroku, select Github under deployment method and link to the repository you have just created.
5. Under Resources, add Postgres to addons.
6. Set up a public AWS S3 bucket to use for static file storage. See [AWS docs](https://docs.aws.amazon.com/index.html?nc2=h_ql_doc#lang/en_us)
7. Set up a [Stripe](https://stripe.com/gb) account.
8. In Heroku, add the following environment variables:
	- AWS_SECRET_ACCESS_KEY - This will come from your AWS S3 bucket
	- AWS_ACCESS_KEY_ID - This will come from your AWS S3 bucket
	- COMPANY_EMAIL - the full email address where you would like the messages in the Contact page to be sent.
	- DISABLE_COLLECTSTATIC - This needs to be set to 1 to be compatible with the AWS bucket.
	- EMAIL_USER - The username of the email address to send forgotten password emails from. This is currently setup as GMAIL but can be edited in settings.py if necessary.
	- EMAIL_PASSWORD - password for the above.
	- SECRET_KEY - The secret key for the django application. Can be any string.
	- STRIPE_PUBLISHABLE - This will come from your Stripe account setup
	- STRIPE_SECRET - This will come from your Stripe account setup.
9. Under the Deploy tab, choose the master branch and select Deploy Branch.
10. Add a file into the main issuetracker folder (where manage.py is) on your local environment called env.py and import this into issuetracker/settings.py. 
11. In env.py, add `os.environ.setdefault("SECRET_KEY", "<yoursecretkey>")` and `os.environ.setdefault("DATABASE_URL", "<database url from heroku")` (don't forget to `import os`) and save it.
12. From your command line, type `python manage.py createsuperuser` and enter desired credentials.
13. Now go to <yourliveapp.herokuapp.com>/admin and log in with the superuser credentials.
14. Go to Users > Add User and create a user with username 'unassigned' (all lower case), and name of 'Not currently assigned' or similar. This is for the application to use as a default staff assignment for all tickets. Give the user staff status.
15. Go back to the admin home, then Developer Profiles > add, and add the new unassigned user. It is vital that this is done before any other user is given a developer profile.
16. Create a developer profile for the superuser.
17. Application deployment is complete.

## Credits
This project was completed as part of the milestone projects in Code Institute's Full Stack Web Development course. The idea is from the brief given for milestone 5, Full Stack Frameworks, although doesnt match the brief exactly, as explained above.

### Media
All images are taken from stock photo websites and are watermarked accordingly, except for the admin's avatar image, which was created using https://avatarmaker.com/.

### Other
The python snippet for the sendMail function was found at https://wsvincent.com/django-contact-form/