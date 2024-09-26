from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import spacy


# Carrega as variaveis de hambiente
load_dotenv()

# Inicia a aplicação Flask
app = Flask(__name__)

# Importa as configurações do app do arquivo confg.py
app.config.from_object('config')

# Inicia o db
db = SQLAlchemy()
db.init_app(app)

# Inicia o spacy
npl = spacy.load('pt_core_news_sm')

from app.services.db.limpa_conversas import Ausencia

c_db = Ausencia(db, 120)
c_db.init_task()

# Inicia o migrate
migrate = Migrate(app, db)

# Carrega os controllers
from app.controllers.entrada import index

# Carrega os models
from app.models.banco import arvore
from app.models.banco import variaveis
from app.models.banco import motivos