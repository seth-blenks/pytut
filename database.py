from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(225))
	email = db.Column(db.String(225), unique=True)

	_authenticated = db.Column(db.Boolean, default = False)
	_active = db.Column(db.Boolean, default=True)
	_password = db.Column(db.String(225))

	@property
	def is_authenticated(self):
		return self._authenticated

	@is_authenticated.setter
	def is_authenticated(self, value):
		self._authenticated = value
		db.session.add(self)

	@property
	def is_active(self):
		return self._active

	@is_active.setter
	def is_active(self, value):
		self._active = value
		db.session.add(self)

	@property
	def password(self):
		return AttributeError('Password is not readable')

	@password.setter
	def password(self, value):
		self._password = generate_password_hash(value)
		db.session.add(self)

	def check_password(self, value):
		return check_password_hash(self._password, value)


tag_post = db.Table(
	'tag_post',
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	)

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(225), unique=True)
	content = db.Column(db.Text)
	date = db.Column(db.DateTime, default=datetime.now)
	image_name = db.Column(db.Text)
	description = db.Column(db.Text)
	_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
	tags = db.relationship('Tag', secondary=tag_post, backref=db.backref('posts'))

	def add_tag(self, tags):
		for tag in tags:
			tag = Tag.query.filter_by(name=tag).first()
			if tag:
				self.tags.add(tag)

	def get_tags(self):
		tags = [x.name for x in self.tags]
		the_tag = ','.join(tags)
		print(the_tag)
		return the_tag


class Tag(db.Model):
	__tablename__ = 'tag'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(225), unique=True)
	

class Comment(db.Model):
	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	message = db.Column(db.Text)
	_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	post = db.relationship('Post', backref=db.backref('comments', lazy='dynamic'))

class Image(db.Model):
	__tablename__ = 'image'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)			
	name = db.Column(db.Text, unique=True)

