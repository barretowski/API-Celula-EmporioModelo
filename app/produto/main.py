from fastapi import FastAPI
from routes.routeProduto import router as produto_router
from routes.routeCategoria import router as categoria_router
from database import engine, Base

app = FastAPI(
    title="Célula Produto",
    description="Gerenciamento de Produtos e Categorias",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)
app.include_router(produto_router, prefix="/produto", tags=["Produto"])
app.include_router(categoria_router, prefix="/categoria", tags=["Categoria"])