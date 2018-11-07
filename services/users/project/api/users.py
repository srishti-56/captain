# services/users/project/api/users.py


from flask import Blueprint, jsonify, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask import redirect, url_for, session

from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from project.api.models import Student
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
    if current_user.is_authenticated:
        print("is authenticated!")
        return redirect(url_for('index'))
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
@users_blueprint.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    print("in gcallback!")
    if current_user is not None and current_user.is_authenticated:
        print("is auth already")
        return redirect(url_for('index'))
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
                user = Student()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'
