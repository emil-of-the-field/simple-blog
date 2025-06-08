import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import extract
from app import create_app, db
from app.models import User, Post
from datetime import datetime

app = create_app()

@app.context_processor
def utility_processor():
    def get_ordered_posts():    
        user = db.session.scalar(sa.select(User, 1))
        query = user.posts.select().order_by(Post.timestamp.desc())
        sorted_posts = db.session.scalars(query).all()
        return sorted_posts
    return dict(get_ordered_posts=get_ordered_posts)

@app.context_processor
def utility_processor():
    def get_tags():
        user = db.session.scalar(sa.select(User, 1))
        query = user.posts.select(Post.tag_names)
        tags = db.session.scalars(query).all()
        return tags
    return dict(get_tags=get_tags)

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
