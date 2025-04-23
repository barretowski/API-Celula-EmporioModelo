from sqlalchemy import Column, Integer, String
from database import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)