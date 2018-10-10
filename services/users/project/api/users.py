# services/users/project/api/users.py


from flask import Blueprint, jsonify, request, render_template
from project.api.models import Student
from sqlalchemy import exc
from project import db

users_blueprint = Blueprint('users', __name__, template_folder='./templates')

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