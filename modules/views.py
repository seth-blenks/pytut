from . import client
from . import login
from flask import render_template, request, abort
from database import Tag, Post


@client.route('/')
def homepage():
	return render_template('homepage.html')

@client.route('/posts')
def posts():
	tag = request.args.get('tag')
	page = request.args.get('page',1, type=int)
	pagination = None
	if tag:
		tag = Tag.query.filter_by(name=tag.strip(' ')).first()
		if tag:
			pagination = Post.query.filter(Post.tags.contains(tag)).paginate(page,12,error_out=False)
	
	if pagination == None:
		pagination = Post.query.order_by(Post.id.desc()).paginate(page,12,error_out=False)

	return render_template('tutorials.html',pagination=pagination)

@client.route('/posts/<title>.html')
def read(title):
	post = Post.query.filter_by(title=title).first()
	if not post:
		abort(404)

	return render_template('read.html',post=post)

@client.route('/contact')
def contact():
	return render_template('contact.html')
