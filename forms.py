from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField

class LoginForm(FlaskForm):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	submit = SubmitField('submit')

class UploadForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	textarea = StringField('textarea', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired()])
	image_name = StringField('image name', validators=[DataRequired()])
	tags = StringField('tags', validators=[DataRequired()])
	submit = SubmitField('submit')

class EditPostForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	tags = StringField('tags', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired()])
	textarea = StringField('textarea', validators=[DataRequired()])
	image_name = StringField('image name', validators=[DataRequired()])
	submit = SubmitField('submit')

class UploadTag(FlaskForm):
	tag = StringField('tag', validators=[DataRequired()])

	