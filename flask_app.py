from flask import Flask
import os
from modules.login import login_manager
from modules import client
from database import db
from pathlib import Path

app = Flask(__name__)

class Basic:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(__file__) + '/db.sqlite'
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	SECRET_KEY = 'O1RXY-hl2LHpr20lneFKw_DlTLCQhTMGCp1ljPZ8j-w'

	BASE_DIR_NAME = os.path.dirname(__file__) + os.path.sep + 'static'+ os.path.sep + 'img'+ os.path.sep + 'gallery'+ os.path.sep + 'uploads'+ os.path.sep + ''

	MAIL_SERVER = 'localhost'
	MAIL_PORT = 2500
	MAIL_USE_TLS = False
	MAIL_USE_SSL = False
	MAIL_DEBUG = app.debug
	MAIL_USERNAME = 'sethmail@pytut.com'
	MAIL_PASSWORD = None
	MAIL_DEFAULT_SENDER = 'sethmail@pytut.com'
	MAIL_MAX_EMAILS = 25
	MAIL_SUPPRESS_SEND = app.testing

app.config.from_object(Basic)



db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(client)


@app.errorhandler(404)
def page_not_found(e):
	return 'page_not_found',404

@app.errorhandler(500)
def server_error(e):
	return 'server error',500

@app.cli.command('setup')
def setup():
	from database import User

	db.drop_all()
	db.create_all()

	seth = User(email='sethdad224@gmail.com',name='seth')
	seth.password = 'password'
	db.session.add(seth)
	db.session.commit()

	from faker import Faker
	from database import User,Post,Tag
	from random import choice


	fake = Faker()

	tags = ['chemistry','biology','english','mathematics','physics','psychology']

	for tag in tags:
		db.session.add(Tag(name=tag))

	db.session.commit()

	for a in range(100):
		post = Post(
			title=fake.user_name(),
			description= fake.user_name(),
		 content=fake.text(),
		  image_name = choice(['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','0.6.jpg'])
		  )
		post.author = User.query.get(1)
		post.tags.append(choice(Tag.query.all()))
		  

		db.session.add(post)

	db.session.commit()


	print('done')


if __name__ == '__main__':
	app.run(debug=True, port=9000)