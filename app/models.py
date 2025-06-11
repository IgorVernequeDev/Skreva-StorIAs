from . import db

class Historias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historia = db.Column(db.Text, nullable=False)
    dificuldade = db.Column(db.String(20), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.now())
    coerencia = db.Column(db.String(20), nullable=False)
    diversao = db.Column(db.String(20), nullable=False)
    gramatica = db.Column(db.String(20), nullable=False)
    moral = db.Column(db.String(20), nullable=False)
    relacaofrase = db.Column(db.String(20), nullable=False)
    media = db.Column(db.String(20), nullable=False)
    frase = db.Column(db.Text, nullable=False)