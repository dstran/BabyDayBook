from mongoengine import *


class Checkup(Document):
    weight = FloatField(required=True)
    weight_percent = IntField(required=True)
    height = FloatField(required=True)
    height_percent = IntField(required=True)
    head_cir = FloatField(required=True)
    head_cir_percent = IntField(required=True)
    notes = StringField(required=True)