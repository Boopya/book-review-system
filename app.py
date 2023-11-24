from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.book_review_system_db

reviews_col = db.reviews

@app.route('/', methods=['GET'])
def index():
    reviews_list = list(reviews_col.find())
    print(reviews_list)
    return render_template('index.html', reviews=reviews_list)

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        title = request.form['title']
        review = request.form['review']
        rating = request.form['rating']
        data = {'title': title, 'review': review, 'rating': rating}
        reviews_col.insert_one(data)
        return redirect(url_for('index'))
    return render_template('add_review.html')
    
@app.route('/<id>/edit_review', methods=['GET', 'POST'])
def edit_review(id):
    review = reviews_col.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        new_title = request.form['title']
        new_review = request.form['review']
        new_rating = request.form['rating']
        reviews_col.update_one({'_id': ObjectId(id)}, {'$set': {'title': new_title, 'review': new_review, 'rating': new_rating}})
        return redirect(url_for('index'))
    return render_template("edit_review.html", old_review=review)

@app.route('/<id>/del_review', methods=['GET'])
def del_review(id):
    reviews_col.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))
