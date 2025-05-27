from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True)
    createdAt = DateTimeField(default=datetime.utcnow)
    lastLogin = DateTimeField()

    meta = {'collection': 'users'}
