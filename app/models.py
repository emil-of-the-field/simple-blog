from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import Table, Column, ForeignKey, ARRAY
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from slugify import slugify


tags_table = Table(
    'tags_assocation', db.metadata,
    sa.Column('post_id', sa.Integer(), sa.ForeignKey('post.id'), primary_key=True),
    sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tag.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Tag(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    posts: so.WriteOnlyMapped['Post'] = so.relationship(secondary=tags_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag> {self.name}'
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    slug: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, default='', nullable=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text())
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    
    tags: so.Mapped[Tag] = so.relationship(secondary=tags_table, back_populates='posts')
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
    def __init__(self, title, body, tags, author):
        self.body = body
        self.title = title
        self.slug = slugify(title)
        self.tags = tags
        self.author = author

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))