from . import db
from sqlalchemy.sql import func

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    Anxiety = db.Column(db.Float)
    Depresi = db.Column(db.Float)
    Lonely = db.Column(db.Float)
    Normal = db.Column(db.Float)
    rekomendasi = db.Column(db.String(10000))
