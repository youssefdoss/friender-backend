'''SQLAlchemy models for Friender.'''

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://r29-friender.s3.us-west-1.amazonaws.com/default.png'

class Likes(db.Model):
    '''Connection of a liker and a liked_user'''

    __tablename__ = 'likes'

    user_being_liked_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True,
    )

    user_liking_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True,
    )

class Dislikes(db.Model):
    '''Connection of a disliker and a disliked_user'''

    __tablename__ = 'dislikes'

    user_being_disliked_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True,
    )

    user_disliking_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True,
    )

class User(db.Model):
    '''User in the system'''

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    bio = db.Column(
        db.Text,
    )

    location = db.Column(
        db.Integer,
        nullable=False,
    )

    radius = db.Column(
        db.Integer,
        default=10000
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    likers = db.relationship(
        'User',
        secondary='likes',
        primaryjoin=(Likes.user_being_liked_id == id),
        secondaryjoin=(Likes.user_liking_id == id),
        backref='liking',
    )
    dislikers = db.relationship(
        'User',
        secondary='dislikes',
        primaryjoin=(Dislikes.user_being_disliked_id == id),
        secondaryjoin=(Dislikes.user_disliking_id == id),
        backref='disliking',
    )

    def __repr__(self):
        return f'<User #{self.id}: {self.first_name} {self.last_name} {self.email}>'

    @classmethod
    def signup(cls, email, first_name, last_name, location, password, radius, bio=None, image_url=DEFAULT_IMAGE_URL):
        '''Sign up user.

        Hashes password and adds user to system.
        '''

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            location=location,
            radius=radius,
            bio=bio,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        '''Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        '''

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def get_display_info(self):
        '''Gets display info for a user'''
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'imageUrl': self.image_url,
            'bio': self.bio,
            'distance': self.distance,
        }

    def get_matches(self):
        '''Gets all matches for a user'''
        liked_user_ids = set([user.id for user in self.liking])
        liked_by_user_ids = set([user.id for user in self.likers])
        matches = list(liked_by_user_ids.intersection(liked_user_ids))

        return matches

    def serialize_display(self, match):
        '''Serialize other user object'''
        return {
            'id': match.id,
            'email': match.email,
            'firstName': match.first_name,
            'imageUrl': match.image_url,
            'bio': match.bio,
            'location': match.location,
            'radius': match.radius,
        }

    def serialize(self):
        '''Serialize self user object'''
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'imageUrl': self.image_url,
            'bio': self.bio,
            'location': self.location,
            'radius': self.radius,
        }
def connect_db(app):
    '''Connect this database to provided Flask app.

    You should call this in your Flask app.
    '''

    app.app_context().push()
    db.app = app
    db.init_app(app)