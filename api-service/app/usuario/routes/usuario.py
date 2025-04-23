from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario
from typing import Optional
from schemas import UsuarioCreate, UsuarioResponse, Login
from auth.security import gerar_hash_senha, criar_token_jwt, verificar_senha

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_root():
    return {"message": "Bem-vindo à API!"}

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
def login(login: Login, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.user == login.user).first()
    if not usuario or not verificar_senha(login.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = criar_token_jwt({"sub": usuario.user})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/obter/")
def obter(nome: Optional[str] = None, usuario: Optional[str] = None, cpf: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Usuario)
    
    if nome:
        query = query.filter(Usuario.nome == nome)
    if usuario:
        query = query.filter(Usuario.user == usuario)
    if cpf:
        query = query.filter(Usuario.cpf == cpf)
    if email:
        query = query.filter(Usuario.email == email)
    
    usuario_encontrado = query.first()  # Retorna o primeiro que corresponder ao filtro
    
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario_encontrado

@router.put("/atualizar/{usuario_id}/", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.nome:
        usuario_existente.nome = usuario.nome
    if usuario.cpf:
        usuario_existente.cpf = usuario.cpf
    if usuario.email:
        usuario_existente.email = usuario.email
    if usuario.user:
        usuario_existente.user = usuario.user
    if usuario.senha:
        usuario_existente.senha = gerar_hash_senha(usuario.senha)
    
    db.commit()
    db.refresh(usuario_existente)
    
    return usuario_existente

@router.delete("/deletar/{usuario_id}/")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(usuario_existente)
    db.commit()
    
    return {"message": "Usuário deletado com sucesso"}
