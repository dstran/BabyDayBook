from mongoengine import *


class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)