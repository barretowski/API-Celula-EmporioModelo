from pydantic import BaseModel

class CategoriaBase(BaseModel):
    descricao: str

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True