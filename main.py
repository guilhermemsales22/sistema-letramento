from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional

DATABASE_URL = "postgresql://postgres:Acfs120625@localhost:5432/letramento_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Configuração do CORS (deve vir antes das rotas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ESQUEMAS DE DADOS (PYDANTIC)
# ==========================================
class LoginSchema(BaseModel):
    email: str
    senha: str

class AlunoUpdateSchema(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[str] = None

class AvaliacaoSchema(BaseModel):
    aluno_id: int
    periodo: str
    nivel_letramento: str
    habilidades_adquiridas: str
    pontos_estimulo: str
    data_avaliacao: str
# ==========================================
# ROTAS DE AUTENTICAÇÃO E LOGIN
# ==========================================
@app.post("/login")
def fazer_login(dados: LoginSchema, db: Session = Depends(get_db)):
    query = text("SELECT id, nome, email FROM usuarios WHERE email = :email AND senha = :senha")
    usuario = db.execute(query, {"email": dados.email, "senha": dados.senha}).fetchone()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
        
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }

# ==========================================
# LÓGICA DE NEGÓCIO E EVOLUÇÃO
# ==========================================
PESOS_LETRAMENTO = {
    "GA": 1,
    "PS": 2,
    "SSV": 3,
    "SCV": 4,
    "SA": 5,
    "AL": 6
}

def calcular_evolucao(nivel_inicial: str, nivel_final: str) -> str:
    peso_ini = PESOS_LETRAMENTO.get(nivel_inicial, 1)
    peso_fin = PESOS_LETRAMENTO.get(nivel_final, 1)
    diferenca = peso_fin - peso_ini
    
    if diferenca >= 2:
        return "↑ Significativa"
    elif diferenca == 1:
        return "↑ Progressiva"
    elif diferenca == 0:
        return "→ Em consolidação"
    else:
        return "↓ Requer atenção"

# ==========================================
# ROTAS DE ALUNOS E HISTÓRICO
# ==========================================
@app.get("/alunos/{aluno_id}/historico")
def obter_historico_aluno(aluno_id: int):
    return {
        "aluno": {
            "id": aluno_id,
            "nome": "Joãozinho da Silva",
            "data_nascimento": "2018-05-10"
        },
        "historico": [
            {
                "id": 1,
                "data": "2026-04-01",
                "descricao": "Joãozinho demonstra ótima evolução nas atividades iniciais de letramento."
            }
        ]
    }

@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, dados: AlunoUpdateSchema, db: Session = Depends(get_db)):
    query_check = text("SELECT id FROM alunos WHERE id = :id")
    aluno = db.execute(query_check, {"id": aluno_id}).fetchone()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    query_update = text("""
        UPDATE alunos 
        SET nome = COALESCE(:nome, nome), 
            data_nascimento = COALESCE(:data_nascimento, data_nascimento)
        WHERE id = :id
    """)
    db.execute(query_update, {
        "id": aluno_id, 
        "nome": dados.nome, 
        "data_nascimento": dados.data_nascimento
    })
    db.commit()
    
    return {"mensagem": "Dados do aluno atualizados com sucesso!"}
@app.post("/avaliacoes")
def cadastrar_avaliacao(dados: AvaliacaoSchema, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    query_aluno = text("SELECT id FROM alunos WHERE id = :id")
    aluno = db.execute(query_aluno, {"id": dados.aluno_id}).fetchone()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Insere a nova avaliação no banco
    query_insert = text("""
        INSERT INTO avaliacoes (aluno_id, periodo, nivel_letramento, habilidades_adquiridas, pontos_estimulo, data_avaliacao)
        VALUES (:aluno_id, :periodo, :nivel_letramento, :habilidades_adquiridas, :pontos_estimulo, :data_avaliacao)
    """)
    
    db.execute(query_insert, {
        "aluno_id": dados.aluno_id,
        "periodo": dados.periodo,
        "nivel_letramento": dados.nivel_letramento,
        "habilidades_adquiridas": dados.habilidades_adquiridas,
        "pontos_estimulo": dados.pontos_estimulo,
        "data_avaliacao": dados.data_avaliacao
    })
    db.commit()
    
    return {"mensagem": "Avaliação cadastrada com sucesso!"}