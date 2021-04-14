from . import client
from forms import UploadForm, EditPostForm
from database import Post, Tag
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
from flask import flash, current_app, request, abort, jsonify
import json
from database import db, Image
from uuid import uuid4
from os import path
from pathlib import Path

def flash_error(form):
	msg = ''
	for field, errors in form.errors.items():
		for error in errors:
			msg += f'{field}: {error} <br>'
	if msg:
		flash(msg, category='alert alert-warning')

@client.route('/admin')
@login_required
def admin_homepage():
	return render_template('admin/homepage.html')

@client.route('/admin/upload', methods=['POST','GET'])
@login_required
def admin_upload():
	form = UploadForm()
	if form.validate_on_submit():

		title = form.title.data.strip(' ')
		old = Post.query.filter_by(title=title).first()

		if old:
			flash('Title already in use', category='alert alert-info')
			return redirect(url_for('client.admin_upload'))

		new_post = Post()
		new_post.title = title
		content = form.textarea.data
		new_post.content = content
		new_post.image_name = form.image_name.data
		new_post.description = form.description.data

		tags = form.tags.data.strip(' ').split(',')
		for tag in tags:
			tag = Tag.query.filter_by(name=tag).first()
			if tag:
				new_post.tags.append(tag)

		new_post.author = current_user
		db.session.add(new_post)
		db.session.commit()

		flash('Post uploaded', category='alert alert-success')
		return redirect(url_for('client.admin_upload'))
	else:
		flash_error(form)

	return render_template('admin/upload.html', form=form)

@client.route('/admin/edit', methods=['POST','GET'])
@login_required
def admin_edit():
	post_id = request.args.get('post_id')
	post = Post.query.get(post_id)
	if not post:
		abort(400)

	form = EditPostForm()

	if form.validate_on_submit():
		title = form.title.data.strip(' ')
		old_post = Post.query.filter(Post.title == title).filter(Post.id != post.id).first()

		if old_post:
			flash('Title already in use', category='alert alert-info')
			return redirect(url_for('client.admin_edit', post_id=post.id))

		post.title = title
		content = form.textarea.data
		current_app.logger.debug(content)
		post.content = content
		post.image_name = form.image_name.data
		post.description = form.description.data
		
		tags = form.tags.data.strip(' ').split(',')
		for tag in tags:
			tag = Tag.query.filter_by(name=tag).first()
			if tag:
				post.tags.append(tag)

		post.author = current_user
		db.session.add(post)
		db.session.commit()

		flash('Post updated successfully', category='alert alert-success')
		return redirect(url_for('client.admin_edit',post_id=post.id))

	else:
		flash_error(form)

	return render_template('admin/edit.html', form=form, post=post)


@client.route('/admin/delete', methods=['POST','GET'])
@login_required
def admin_delete():
	post_id = request.args.get('post_id')
	post = Post.query.get(int(post_id))

	if not post:
		abort(400)

	db.session.delete(post)
	db.session.commit()

	flash('post deleted')

	return redirect(url_for('client.admin_homepage'))

@client.route('/admin/tag',methods=['POST','GET'])
@login_required
def admin_tag():
	if request.method == 'GET':
		tags = Tag.query.all()
		data = []
		for tag in tags:
			data.append(tag.name)

		return jsonify(data)

	tags = request.form.get('tags')
	if not tags:
		abort(400)

	for tagname in tags.split(','):
		tag = Tag.query.filter_by(name=tagname).first()
		current_app.logger.debug(tag)
		if not tag:
			db.session.add(Tag(name=tagname.lower()))

	db.session.commit()

	return 'Done'

@client.route('/admin/image', methods=['POST','GET'])
@login_required
def admin_image():

	if request.method == 'GET':
		page = request.args.get('page',1,type=int)
		_type = request.args.get('type')
		images = Image.query.paginate(page,5,error_out=False).items

		data = []
		for image in images:
			data.append(image.name)

		return jsonify(data)

	
	_file = request.files.get('image')

	if not _file:
		abort(400)

	extension = _file.filename.split('.')[-1]
	filename = str(uuid4()) + '.' + extension

	new_image = Image(name=filename)
	file_path = current_app.config['BASE_DIR_NAME']+ filename
	with open(file_path,'wb') as wfile:
		wfile.write(_file.read())

	db.session.add(new_image)
	db.session.commit()

	flash('Image upload successful', category='alert alert-success')
	return redirect(url_for('client.admin_upload'))

