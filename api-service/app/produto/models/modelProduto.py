from sqlalchemy import Column, Integer, String, Float
from database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    categoriaId = Column(Integer, nullable=True)
    valor = Column(Float, nullable=True)
    quantidade = Column(Float, nullable=True)
    imagem = Column(String, nullable=True)
    codigoBarras = Column(String, nullable=True)
    codigo = Column(Integer, nullable=True)