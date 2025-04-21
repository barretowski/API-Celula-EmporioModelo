from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.modelProduto import Produto
from schemas.schemaProduto import ProdutoBase, ProdutoResponse
from logger import logger
from typing import List

router = APIRouter()

@router.post("/inserir/", response_model=ProdutoResponse)
def inserir_produto(produto: ProdutoBase, db: Session = Depends(get_db)):
    try:
        db_produto = Produto(
            nome=produto.nome,
            descricao=produto.descricao,
            categoriaId=produto.categoriaId,
            valor=produto.valor,
            quantidade=produto.quantidade,
            imagem=produto.imagem,
            codigoBarras=produto.codigoBarras,
            codigo=produto.codigo
        )
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        logger.info(f"Produto '{db_produto.nome}' inserido com sucesso.")
        return db_produto
    except Exception as e:
        logger.error(f"Erro ao inserir produto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inserir produto")

@router.get("/obter/", response_model=List[ProdutoResponse])
def obter_produtos(db: Session = Depends(get_db)):
    try:
        produtos = db.query(Produto).all()
        return produtos
    except Exception as e:
        logger.error(f"Erro ao obter produtos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter produtos")

@router.get("/obter/{produto_id}/", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

@router.put("/alterar/{produto_id}/", response_model=ProdutoResponse)
def alterar_produto(produto_id: int, produto: ProdutoBase, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto_existente:
        logger.warning(f"Tentativa de atualizar produto com ID {produto_id}, mas não foi encontrado.")
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto_existente.nome = produto.nome
    produto_existente.descricao = produto.descricao
    produto_existente.categoriaId = produto.categoriaId
    produto_existente.valor = produto.valor
    produto_existente.quantidade = produto.quantidade
    produto_existente.imagem = produto.imagem
    produto_existente.codigoBarras = produto.codigoBarras
    produto_existente.codigo = produto.codigo
    
    db.commit()
    db.refresh(produto_existente)
    logger.info(f"Produto com ID {produto_id} atualizado com sucesso.")
    return produto_existente

@router.delete("/deletar/{produto_id}/")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto_existente:
        logger.warning(f"Tentativa de deletar produto com ID {produto_id}, mas não foi encontrado.")
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(produto_existente)
    db.commit()
    logger.info(f"Produto com ID {produto_id} deletado com sucesso.")
    return {"message": "Produto deletado com sucesso"}
