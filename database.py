# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o PostgreSQL
# Formato: postgresql://usuario:senha@localhost:5432/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Acfs120625@localhost:5432/letramento_db"

# Engine é o motor que gerencia as conexões
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal é cada "conversa" individual com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criarmos nossos modelos Python depois
Base = declarative_base()

# Dependência que usaremos nas rotas para pegar a conexão e fechar depois
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()