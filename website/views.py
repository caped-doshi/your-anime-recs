from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Anime_Rating
from . import db
import sys
import pandas as pd
from item_based import fill_df, recommend_movies
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
import asyncio
from dotenv import load_dotenv
from os import getenv
load_dotenv()

uri = getenv('uri')
client = MongoClient(uri)
mongo_db = client.get_database("ratings")
collection = mongo_db.get_collection("anime")

views = Blueprint('views', __name__)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    s = ""
    if request.method == 'POST':
        print(request.form)
        anime = request.form.get('name')
        rating = request.form.get('rating_'+anime)
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
    new_arr = []
    if request.method == 'POST':
        anime = collection.find_one({"_id":"all_anime"})['arr']
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
        cursor = collection.find({})
        genres = []
        for anime in cursor:
            if anime['_id'] != 'all_anime':
                genres.append(anime['genres'])
        print(genres)
        df1, sim_movies_dict = fill_df(df, current_user.id, genres)
        arr = recommend_movies(current_user.id, df,df1,5)
        new_arr = []
        for a in arr:
            tup = (a[0], a[1], sim_movies_dict[a[0]])
            new_arr.append(tup)
            
    return render_template("recommendations.html", user=current_user, a_list = new_arr)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/get_anime_list', methods=['POST'])
def get_anime_list():
    cursor = collection.find_one({"_id":"all_anime"})
    j = jsonify(cursor['arr'])
    return j

@views.route('/get_rating', methods=['POST'])
def get_rating():
    anime_rating = Anime_Rating.query.filter_by(user_id=current_user.id)
    anime_rating_dict = {}
    for rating in anime_rating:
        rating = rating.__dict__
        anime_rating_dict[rating['name']] = rating['rating']
    return anime_rating_dict

@views.route('/get_anime_details', methods=['POST'])
def get_anime_details():
    cursor = collection.find({})
    d = {}
    for anime in cursor:
        if anime['_id'] != 'all_anime':
            img = anime['image']
            img = img.replace('67','134')
            img = img.replace('98','196')
            d[anime['_id']] = (anime['rating'], anime['description'], img, anime['genres'])
    return d