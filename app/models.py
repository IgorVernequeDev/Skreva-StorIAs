from . import db

from datetime import datetime
import pytz

# Fuso horário de São Paulo
fuso_sp = pytz.timezone('America/Sao_Paulo')

def horario_sp():
    return datetime.now(fuso_sp)

class Historias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historia = db.Column(db.Text, nullable=False)
    dificuldade = db.Column(db.String(20), nullable=False)
    data_criacao = db.Column(db.DateTime, default=horario_sp)
    coerencia = db.Column(db.String(20), nullable=False)
    diversao = db.Column(db.String(20), nullable=False)
    gramatica = db.Column(db.String(20), nullable=False)
    moral = db.Column(db.String(20), nullable=False)
    relacaofrase = db.Column(db.String(20), nullable=False)
    media = db.Column(db.String(20), nullable=False)
    frase = db.Column(db.Text, nullable=False)