from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importando os elementos definidos no modelo
from model.base import Base
from .plano import Plano

db_path = "database/"
# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # Então cria o diretório
    os.makedirs(db_path)

# URL de acesso ao banco (essa é uma URL de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)