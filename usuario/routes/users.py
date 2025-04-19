from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse
from auth.security import gerar_hash_senha, criar_token_jwt, verificar_senha

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cadastro/", response_model=UsuarioResponse)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.user == usuario.user).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Nome de Usuário já cadastrado")
    
    usuario.senha = gerar_hash_senha(usuario.senha)
    novo_usuario = Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login/")
def login(user: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.user == user).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = criar_token_jwt({"sub": usuario.user})
    return {"access_token": token, "token_type": "bearer"}
