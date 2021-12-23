from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Anime_Rating
from . import db
import sys
import pandas as pd
from item_based import fill_df, recommend_movies

views = Blueprint('views', __name__)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    s = ""
    if request.method == 'POST':
        print(request.form)
        anime = request.form.get('name')
        rating = request.form.get('rating')
        s = request.form.get('search_bar')
        r = float(rating)

        anime_rating = Anime_Rating.query.filter_by(
            name=anime, user_id=current_user.id).first()
        if(anime_rating):
            db.session.delete(anime_rating)
            db.session.commit()
            new_rating = Anime_Rating(
                name=anime, rating=rating, user_id=current_user.id)
            db.session.add(new_rating)
            db.session.commit()
            flash(f"Changed your previous rating of {anime}", category="success")
        else:
            print("couldn't find in db", file=sys.stdout)
            new_rating = Anime_Rating(
                name=anime, rating=r, user_id=current_user.id)
            db.session.add(new_rating)
            db.session.commit()

    return render_template("search.html", user=current_user, search=s)

@views.route('/recommendation', methods=['GET', 'POST'])
@login_required
def recommend():
    arr = []
    if request.method == 'POST':
        anime = ['Naruto', 'One Piece', 'My Hero Academia', 'Attack on Titan','Hunter X Hunter']
        data = {}
        ratings = Anime_Rating.query.all()
        for rating in ratings:
            user = rating.user_id
            anime_index = anime.index(rating.name)
            r = rating.rating
            if user not in data:
                temp_arr = [0 for i in range(len(anime))]
                data[user] = temp_arr
            data[user][anime_index] = r
        df = pd.DataFrame(index=anime, columns=data, data=data)
        print(df)
        df1 = fill_df(df, current_user.id)
        print(df1)
        arr = recommend_movies(current_user.id, df,df1,2)
        print(arr)
            
    return render_template("recommendations.html", user=current_user, a_list = arr)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)