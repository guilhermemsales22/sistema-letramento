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
@app.get("/alunos/{aluno_id}/historico", status_code=200)
def obter_historico_aluno(aluno_id: int, db: Session = Depends(get_db)):
    query_aluno = text("SELECT id, nome, turma_id FROM alunos WHERE id = :id")
    aluno = db.execute(query_aluno, {"id": aluno_id}).fetchone()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    query_avaliacoes = text("""
        SELECT id, periodo, nivel_letramento, habilidades_adquiridas, 
               pontos_estimulo, data_avaliacao 
        FROM avaliacoes 
        WHERE aluno_id = :id 
        ORDER BY data_avaliacao ASC
    """)
    avaliacoes = db.execute(query_avaliacoes, {"id": aluno_id}).fetchall()

    evolucao_geral = "Aguardando mais avaliações..."
    if len(avaliacoes) >= 2:
        primeiro_nivel = avaliacoes[0].nivel_letramento
        ultimo_nivel = avaliacoes[-1].nivel_letramento
        evolucao_geral = calcular_evolucao(primeiro_nivel, ultimo_nivel)

    return {
        "aluno_id": aluno.id,
        "nome": aluno.nome,
        "turma_id": aluno.turma_id,
        "evolucao_geral": evolucao_geral,
        "avaliacoes": [
            {
                "id": av.id,
                "periodo": av.periodo,
                "nivel_letramento": av.nivel_letramento,
                "data_avaliacao": str(av.data_avaliacao),
                "habilidades_adquiridas": av.habilidades_adquiridas,
                "pontos_estimulo": av.pontos_estimulo
            } for av in avaliacoes
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