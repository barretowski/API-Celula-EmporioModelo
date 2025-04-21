from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.modelCategoria import Categoria
from models.modelProduto import Produto
from typing import List
from schemas.schemaCategoria import CategoriaBase, CategoriaResponse
from logger import logger 

router = APIRouter()

@router.post("/inserir/", response_model=CategoriaResponse)
def inserir_categoria(categoria: CategoriaBase, db: Session = Depends(get_db)):
    try:
        db_categoria = Categoria(descricao=categoria.descricao)
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        logger.info(f"Categoria '{db_categoria.descricao}' inserida com sucesso.")
        return db_categoria
    except Exception as e:
        logger.error(f"Erro ao inserir categoria: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inserir categoria")

@router.get("/obter/", response_model=List[CategoriaResponse])
def obter_categorias(db: Session = Depends(get_db)):
    try:
        categorias = db.query(Categoria).all()
        logger.info(f"Lista de categorias retornada com sucesso. Total: {len(categorias)} categorias.")
        return categorias
    except Exception as e:
        logger.error(f"Erro ao obter categorias: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter categorias")

@router.get("/obter/{categoria_id}/", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        logger.warning(f"Categoria com ID {categoria_id} não encontrada.")
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    logger.info(f"Categoria com ID {categoria_id} obtida com sucesso.")
    return categoria

@router.put("/alterar/{categoria_id}/", response_model=CategoriaResponse)
def alterar_categoria(categoria_id: int, categoria: CategoriaBase, db: Session = Depends(get_db)):
    categoria_existente = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_existente:
        logger.warning(f"Tentativa de atualizar categoria com ID {categoria_id}, mas não foi encontrada.")
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categoria_existente.descricao = categoria.descricao
    db.commit()
    db.refresh(categoria_existente)
    logger.info(f"Categoria com ID {categoria_id} atualizada com sucesso.")
    return categoria_existente

@router.delete("/deletar/{categoria_id}/")
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria_existente = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_existente:
        logger.warning(f"Tentativa de deletar categoria com ID {categoria_id}, mas não foi encontrada.")
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Atualizando todos os produtos com a categoria sendo deletada
    produtos = db.query(Produto).filter(Produto.categoriaId == categoria_id).all()
    for produto in produtos:
        produto.categoriaId = None
        db.commit() 

    db.delete(categoria_existente)
    db.commit()
    logger.info(f"Categoria com ID {categoria_id} deletada com sucesso, produtos atualizados.")
    return {"message": "Categoria deletada com sucesso, produtos atualizados."}
