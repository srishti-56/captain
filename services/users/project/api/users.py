# services/users/project/api/users.py


from flask import Blueprint, jsonify, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from project.api.models import Student
from sqlalchemy import exc
from project import db

# NOTE: may need to placed in another file such as config.py??
# Please delete above comment if resolved
class Auth:
    CLIENT_ID = ('630861931474-mqa933274lsoctu9r94rb0j4tas2o6r6.apps.googleusercontent.com')
    CLIENT_SECRET = 'gUOr5-q89miUNIwEtTciEC2f'
    REDIRECT_URI = 'http://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://www.googleapis.com/oauth2/v3/token'
    USER_INFO = 'https://www.googleapis.com/auth/userinfo.profile'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    #USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


users_blueprint = Blueprint('users', __name__, template_folder='./templates')

'''
This function
	creates OAuth session object, used by login functions below
'''
# @login_manager.user_loader
# def get_google_auth(state=None, token=None):
#     if token:
#         return OAuth2Session(Auth.CLIENT_ID, token=token)
#     if state:
#         return OAuth2Session(
#             Auth.CLIENT_ID,
#             state=state,
#             redirect_uri=Auth.REDIRECT_URI)
#     oauth = OAuth2Session(
#         Auth.CLIENT_ID,
#         redirect_uri=Auth.REDIRECT_URI,
#         scope=Auth.SCOPE)
#     return oauth

@users_blueprint.route('/', methods=['GET'])
@login_required			# ensures login is required on homepage load and redirects to login page
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('index.html', auth_url=auth_url)

'''
This function 
	Performs Google login to check if user is logged in 
	else authenticate user and login
'''
@users_blueprint.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
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
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
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
