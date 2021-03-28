from hashlib import md5

from bson import ObjectId
from flask_login import UserMixin
from mongoengine import Document, StringField
from werkzeug.security import generate_password_hash, check_password_hash

from api import login


@login.user_loader
def load_user(id_):
    return User.objects(id=id_).first()


class User(UserMixin, Document):

    id = StringField(primary_key=True)
    username = StringField(max_length=64, unique=True)
    email = StringField(max_length=120, unique=True)
    password_hash = StringField(max_length=128)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': 'private!'
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
