from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    categoriaId: Optional[int]
    valor: float
    quantidade: float
    imagem: str
    codigoBarras: str
    codigo: int

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True