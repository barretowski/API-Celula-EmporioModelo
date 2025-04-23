from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana, senha_hashed):
    return pwd_context.verify(senha_plana, senha_hashed)

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_jwt(dados: dict):
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({"exp": expiracao})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
