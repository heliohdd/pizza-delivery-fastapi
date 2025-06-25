from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para conferir a versão do python: python --version
# 1- para rodar o nosso ódigo, executar no terminal: uvicorn main:app --reload
# 2- para acessar a documentação da API em formato OpenAPI: http://127.0.0.1:8000/docs
# instalar as dependencias pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart
# install fastapi e uvicorn, executar no terminal: pip install fastapi uvicorn
# para instalar o SQLAlchemy Utils, executar no terminal: pip install sqlalchemy-utils
# 2- para instalar o Alembic, executar no terminal: pip install alembic
# para inicializar o Alembic, executar no terminal: alembic init alembic
# 4- para criar uma nova migração, executar no terminal: alembic revision --autogenerate -m "nome_da_migração"
# 3- para migrar o banco de dados, executar no terminal: alembic upgrade head
# 5- para ver o histórico de migrações, executar no terminal: alembic history
# 6- para desfazer a última migração, executar no terminal: alembic downgrade -1
# 7- para desfazer todas as migrações, executar no terminal: alembic downgrade base