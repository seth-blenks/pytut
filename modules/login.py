from . import client
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from database import User, db
from forms import LoginForm
from flask import render_template, request, current_app, redirect, url_for, abort, flash

login_manager = LoginManager()
login_manager.login_view = 'client.authenticate_user'
login_manager.login_message = 'login to continue'
login_manager.login_message_category = 'alert alert-info'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@client.route('/login', methods=['POST','GET'])
def authenticate_user():
	form = LoginForm()

	if form.validate_on_submit():
		email =  form.email.data
		user = User.query.filter_by(email=email).first()

		if not user:
			flash('Login failed', category='alert alert-info')
			return redirect(url_for('client.authenticate_user'))

		if user.check_password(form.password.data):
			user.is_authenticated = True
			db.session.add(user)
			db.session.commit()

			remember = request.form.get('remember')
			current_app.logger.debug(remember)

			login_user(user)
			flash('user logged in', category='alert alert-success')

			_next = request.args.get('next')
			if _next:
				return redirect(_next)

			else:
				return redirect(url_for('client.homepage'))

	return render_template('login/login.html',form=form)

@client.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have successfully logged out', category='alert alert-success')
	return redirect(url_for('client.homepage'))