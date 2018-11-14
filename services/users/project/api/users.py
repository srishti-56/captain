# services/users/project/api/users.py

import simplejson as json

from flask import Blueprint, jsonify, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

from flask import redirect, url_for, session

from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from project.api.models import Student, Teacher, User
from sqlalchemy import exc
from project import create_app, db
from project import login_manager


users_blueprint = Blueprint('users', __name__, template_folder='./templates')

'''
This class provides the necessary credentials for Google Auth (login) API key
'''
class Auth:
    CLIENT_ID = ('630861931474-mqa933274lsoctu9r94rb0j4tas2o6r6.apps.googleusercontent.com')
    CLIENT_SECRET = 'gUOr5-q89miUNIwEtTciEC2f'
    REDIRECT_URI = 'https://localhost:5001/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://www.googleapis.com/oauth2/v3/token'
    USER_INFO = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
    # USER_INFO = 'https://www.googleapis.com/oauth2/v3/userinfo?alt=json'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    #USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


'''
This function
	creates OAuth session object, used by login functions below
'''
@login_manager.user_loader
def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

@users_blueprint.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@users_blueprint.route('/users', methods=['POST'])
def add_user():
	post_data = request.get_json()
	response_object = {
		'status': 'fail',
		'message': 'Invalid payload.'
	}
	if not post_data:
		return jsonify(response_object), 400
	usn = post_data.get('usn')
	try:
		user = User.query.filter_by(usn=usn).first()
		if not user:
			db.session.add(User(usn=usn, name=name, email=email, branch=branch, semester=semester, section=section))
			db.session.commit()
			response_object['status'] = 'success'
			response_object['message'] = f'{usn} was added!'
			return jsonify(response_object), 201
		else:
			response_object['message'] = 'Sorry. That USN already exists.'
			return jsonify(response_object), 400
	except exc.IntegrityError as e:
		db.session.rollback()
		return jsonify(response_object), 400
	return render_template('student_profile.html')
'''
This function
	Saves state on user login
'''
@users_blueprint.route('/login')
def login():
    print("in login")
    print(current_user)
    if current_user.is_authenticated:
        print(current_user.name," ", current_user.email, "is authenticated!")
        response_object = {
        'status': 'success',
        'message': 'Already logged in.'
        }
        return jsonify(response_object)
        #return redirect(url_for('users.index'))
    #else
    print("get auth")
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    print(auth_url, state)
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)

'''
This function 
	Performs Google login to check if user is logged in 
	else authenticate user and login
'''

@users_blueprint.route('/profile')
def profile():
    print("Display profile")
    return render_template('student_profile.html')

@users_blueprint.route('/something')
@login_required
def somewhere():
    print("Testing @loginrequired")
    return jsonify()


@users_blueprint.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    print("in gcallback!")
    if current_user is not None and current_user.is_authenticated:
        print("is auth already")
        return redirect(url_for('users.index'))
    if 'error' in request.args:
        print("some error")
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        print("missing?")
        ##!! COMES HERE FOR SOME REASON????
        return redirect(url_for('users.login'))
    else:
        print("trying?")
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
            print(token)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            print(user_data)
            email = user_data['email']
            print(email)
            user = Student.query.filter_by(email=email).first()
            print(email)
            if user is None:
                print("New user! need Details?")
                try:
                    user = Student()
                    user.email = email
                except:
                    print("Error creating new user, init requires 'usn', 'name', 'email', 'branch', 'semester', and 'section' data")
                    return "Error creating new user, init requires 'usn', 'name', 'email', 'branch', 'semester', and 'section' data"                    
                    #return redirect(url_for('users.signup'))
            # try:
            # current_user.is_authenticated = True
            current_user.name = user_data['name']
            current_user.email = user_data['email']
            # current_user.token = token
            print(token)
            user.tokens = json.dumps(token)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            # except: 
            #     print("Error adding user details and logging in")
            #     return 'Error adding user details and logging in'
            
            return redirect(url_for('users.profile'))
        return 'Could not fetch your information.'

@users_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('users.index'))

