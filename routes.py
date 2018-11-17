import os
import secrets
import requests
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from qa_system import app, db, bcrypt, mail 
from qa_system.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from qa_system.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from qa_system.cluster_knowledge import *

import xml.etree.ElementTree as ElementTree
import sys
import re
import string
import math
import numpy
import pickle
import os
import nltk
import random
import json
import threading
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import ne_chunk
from nltk.tree import Tree
from collections import Counter
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm
from scipy.sparse import bsr_matrix
from glob import glob
from flask import Flask
from flask import request
from flask import Response
from flask import flash
from flask_cors import CORS
from werkzeug.utils import secure_filename

post_count = numpy.random.randint(0,10**9+7)

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.paginate(page = page, per_page = 1)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(id=post_count-1, title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Topic',
                           form=form, legend='New Topic')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/questions", methods = ['GET', 'POST'])
@login_required
def add_questions(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Questions()
    if form.validate_on_submit():
        pass


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your topic has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update topic',
                           form=form, legend='Update Topic')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your topic has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/search_results", methods=['POST'])
def search_results():
    print("Search_bar entered")
    query_string = dict(request.form)['search-term'][0]
    print(query_string)
    #form = SearchBar()
    posts = Post.query.filter_by(title=query_string).all()
    print(posts[0].content)
    return render_template('search_results.html', posts=posts)

@app.route("/intermediate_search", methods=["POST"])
def intermediate_search():
    string=request.form["string"]
    print(string)
    # Post.query.filter(Post.title.ilike("%ma%")).all()[0].title
    test = [row.title for row in Post.query.filter(Post.title.contains(string)).all()]
    print(test)
    return json.JSONEncoder().encode(test)

def send_reset_email(user):
    token = User.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token = token, _external = True)}

If you did not make this request, ignore this email.
'''
    mail.send(msg)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).paginate(page = page, per_page = 5)
    return render_template('user_posts.html', posts=posts, user = user)

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user in None:
        flash('That is an invalid / expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)

'''
MODEL STUFF
'''

@app.route("/post/upload_pdf", methods = ["POST"])
def upload_pdf():
    global post_count

    topic_id = str(post_count)
    post_count = numpy.random.randint(0, 10**9 + 7)

    ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    print(request.files)

    if 'file' not in request.files:
        return json_encoder.encode({"message":"Failure", "comment":"No file received"})

    file = request.files['file']
    
    if file.filename == '':
        return json_encoder.encode({"message":"Failure", "comment":"No file selected"})

    if file:
        if allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            string = extract_string_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            threading.Thread(target = train_bot, args = (topic_id, string)).start()

            return json_encoder.encode({"message":"Success", "comment":"File uploaded successfully"})
        else:
            return json_encoder.encode({"message":"Failure", "comment":"File type not allowed"})

    return json_encoder.encode({"message":"Failure", "comment":"Internal Error"})

@app.route("/post/upload_txt", methods = ["POST"])
def upload_txt():
    topic_id = str(post_count)
    post_count += 1

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if 'file' not in request.files:
        return json_encoder.encode({"message":"Failure", "comment":"No file received"})

    file = request.files['file']
    
    if file.filename == '':
        return json_encoder.encode({"message":"Failure", "comment":"No file selected"})

    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            string = extract_string_from_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            threading.Thread(target = train_bot, args = (topic_id, string)).start()

            return json_encoder.encode({"message":"Success", "comment":"File uploaded successfully"})
        else:
            return json_encoder.encode({"message":"Failure", "comment":"File type not allowed"})

    return json_encoder.encode({"message":"Failure", "comment":"Internal Error"})

@app.route("/post/upload_inputted_txt", methods = ["POST"])
def upload_inputted_txt():
    topic_id = str(post_count)
    post_count += 1

    string = request.json['text']
    
    if len(string) == 0:
        return json_encoder.encode({"message":"Failure", "comment":"No text inputted."})

    threading.Thread(target = train_bot, args = (topic_id, string)).start()

    return json_encoder.encode({"message":"Success", "comment":"File uploaded successfully"})

@app.route("/post/get_clustering_progress/<json>", methods = ["GET"])
def get_clustering_progress(json):
    data = json_decoder.decode(json)
    topic_id = data['topic_id']

    if topic_id not in currently_creating_clusters:
        return json_encoder.encode({"message":"Failure", "comment":"No progress in creating clusters in this topic."})

    def get_clustering_progress_streamer():

        while True:

            if currently_creating_clusters[topic_id]['changed']:
                currently_creating_clusters[topic_id]['changed'] = False
                yield "event: CLUSTERING_PROGRESS\ndata: " + (currently_creating_clusters['current_count'] / currently_creating_clusters['max_count']) + "\n\n"

    return Response(get_clustering_progress_streamer(), mimetype = "text/event-stream") 
