You can easily acces via: noviosapp.herokuapp.com

In a terminal window, navigate into your novios directory.

Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages (Flask and SQLAlchemy, for instance) are installed.

Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py. 

Set the environment variable DATABASE_URL to be the URI of your database, which you should be able to see from the credentials page on Heroku. Use set DATABASE_URL = <database URL>

Run flask run to start up your Flask application.
