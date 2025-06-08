from flask import render_template, url_for, redirect, flash, abort, request, current_app
from app import db
from app.main import bp
from app.models import User, Post
from app.main.forms import PostForm
import sqlalchemy as sa
from flask_login import login_required, current_user

@bp.route('/', methods=["GET"])
@bp.route('/index', methods=["GET"])
def index():
    user = db.session.scalar(sa.select(User, 1))
    query = user.posts.select().order_by(Post.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/about')
def about():
    return render_template('about.html', title="About")


@bp.route('/post/create', methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        post = Post(title = form.title.data, body = form.body.data, tags = form.tags.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)

@bp.route('/post/<slug>', methods=["GET"])
def view(slug):
    post = db.first_or_404(sa.select(Post).where(Post.slug == slug))
    return render_template('view_post.html', post=post, title=post.title)

@bp.route('/post/edit/<slug>', methods=["GET", "POST"])
@login_required
def edit(slug):
    post = db.first_or_404(sa.select(Post).where(Post.slug == slug))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.tags = form.tags.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.view', slug=post.slug))
    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body
        form.tags.data = post.tags
    return render_template('edit_post.html', title='Edit Post', post=post, form=form)

@bp.route('/post/delete/<slug>', methods=["GET", "POST"])
@login_required
def delete(slug):
    post = db.first_or_404(sa.select(Post).where(Post.slug == slug))
    form = PostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted')
        return redirect(url_for('main.index'))
    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body
    return render_template('delete_post.html', title='Delete Post', post=post, form=form)
