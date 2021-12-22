from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/search')
@login_required
def search_page():
    return render_template("search.html", user=current_user)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)