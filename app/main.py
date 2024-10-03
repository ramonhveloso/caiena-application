from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.database.base import Base
from app.database.session import engine

app = FastAPI(
    title="Caiena Application",
    description="""Aplicação integrada com o OpenWeatherMap e o Github 
                    para que seja possível enviar um comentário em um Gist 
                    com a temperatura atual e a previsão do tempo dos próximos 
                    cinco dias (média diária) de uma cidade.""",
    version="0.1.0",
)

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Incluir rotas
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
