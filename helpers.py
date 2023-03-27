import os
import urllib.parse
import customcalendar

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def color_dates(monthhtml, dates, themonth):
    days = []
    for x in dates:
        date = x[0]
        month = int(date[5:7])

        if month == themonth:
            days.append(date[8:10])
    
    for y in days:
        day = int(y)
        monthhtml = monthhtml.replace(f"<td>{day}</td>", f"<td style='background-color: green'>{day}</td>")

    return monthhtml