# Habit Tracker
#### Video Demo:  <URL HERE>
#### Description:
This is my final project for the CS50 course by the Harvard University.
My project is web application using Flask and MySQL.
It is a simple App that lets the user keep track of his/her habits.
The user can add, delete and mark completed habits.
Furthermore the user can see the history of a habit, choosing the year and the habit which he wants to see the history of.

#### app.py:
A flask file with several functions.
The self explaining functions are the register, login and logout functions.
The register function first checks for user compliance. Meaning we check if the user provided a username and a password and if the password was confirmed. Next we check if the username is already taken. If it is not taken we then we create a hash for the provided password and store both in our databank.
In the login functions we first check for user compliance. We check if the user exists and if the user exists we check the provided password. If the password is right we create a session for the user and redirect to the index site.
The logout function clears the user session.

The main functions which contain the functionality of the webapp are the index, add_habit, delete_habit, update_habit and the habit_history functions.
The index function checks if the user already has habits stored in the databank. Then it stores it in a table, which is used in the index.html.
The add_habit function stores new habits the user wants to track and saves it in the database
The delete_habit function deletes habits from the database of the user.
The update_habit function saves the date from today and saves it along with the habit in the database so we know if the habit was done for the day.
The habit_history function takes a habit and a year as arguments and searches for dates that fall in that category from the database. It then creates a html calendar in which the dates are colored green. This calendar is then given to the history.html site.

#### templates:
The templates folder contains the html files for the webapp.
It consists of 4 static sites and the layout.html written with Jinja.
We have a register and login site.
The main component is the index site. Here we can add, delete and mark our habits as done. Furthermore you can choose a habit and a year for which you can let the app display your history of streak for that habit.
The history.html renders this in a monthly calendar in which the days are marked green for the days the user marked the habit as done.

#### habits.db:
This database has 3 tables.
users:
this table stores the username of the user and gives it a unique id
habits:
this table stores the habits of the user using the unique id and the name of the habit
tracking:
this table tracks the accomplishments of the user by saving the name of the habit and the date on which the habit was completed.

#### customcalendar.py:
This file contains a custom version of the calendar module from python (https://github.com/python/cpython/blob/3.11/Lib/calendar.py).
This module was modified with bootstrap code to render the calendar for the history.html file. Also it was modified so I could color the dates for the completed dates easier.

#### helpers.py
This file contains 2 functions.
The login_required function which I took from a previous cs50 problem set. And the color dates function which colors the dates on which a habit was completed and returns them with green background.