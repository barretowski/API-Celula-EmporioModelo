from pydantic import BaseModel, field_validator, EmailStr

class UsuarioBase(BaseModel):
    nome: str
    user: str
    cpf: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str
    @field_validator('senha')
    def senha_minima(cls, v):
        if len(v) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres')
        return v

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class Login(BaseModel):
    user: str
    senha: str