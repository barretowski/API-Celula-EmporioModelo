from pydantic import BaseModel, field_validator, EmailStr

class CategoriaBase(BaseModel):
    descricao: str

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True