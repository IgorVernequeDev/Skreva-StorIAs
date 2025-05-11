from app import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frase = db.Column(db.String(255), nullable=False)
    historia = db.Column(db.Text, nullable=False)
    avaliacao = db.Column(db.String(100))