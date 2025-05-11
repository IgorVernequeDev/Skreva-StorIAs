from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Instâncias globais
db = SQLAlchemy()

def create_app():
    # Carrega variáveis de ambiente do .env
    load_dotenv()

    # Cria a instância do Flask
    app = Flask(__name__)

    # Configurações a partir do config.py
    app.config.from_object('config.Config')

    # Inicializa extensões com o app
    db.init_app(app)

    # Importa e registra o blueprint de rotas
    from app.routes.main import main
    app.register_blueprint(main)

    # Retorna o app configurado
    return app