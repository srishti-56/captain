# services/users/manage.py

import unittest

from flask.cli import FlaskGroup

from project import create_app, db   
from project.api.models import Student  

app = create_app()

# creates a new FlaskGroup instance to extend the normal CLI with commands related to the Flask app
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    """ Initializes the database """
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(usn="001", name="abc", email="abc@abc.com", branch="CSE", semester=7, section="A"))
    db.session.add(User(usn="002", name="def", email="def@def.com", branch="CSE", semester=7, section="B"))
    db.session.add(User(usn="003", name="xyz", email="xyz@xyz.com", branch="CSE", semester=7, section="C"))
    db.session.commit()

if __name__ == '__main__':
	cli()