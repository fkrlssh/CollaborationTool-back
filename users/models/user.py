from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField()
    name = StringField(required=True)
    authType = StringField(default='local', choices=('local', 'google'))
    createdAt = DateTimeField(default=datetime.utcnow)
    lastLogin = DateTimeField()

    meta = {'collection': 'users'}
