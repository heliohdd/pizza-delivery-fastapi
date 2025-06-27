from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")  # Default to HS256 if not set  
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Default to 30 minutes if not set

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para conferir a versão do python: python --version
# 1- para rodar o nosso código, executar no terminal: uvicorn main:app --reload
# 2- para acessar a documentação da API em formato OpenAPI: http://127.0.0.1:8000/docs
# instalar as dependencias pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart -> uvicorn(server), fastapi (framework), sqlalchemy (ORM), passlib (hashing de senhas), python-jose (JWT), python-dotenv (variaveis de ambiente), python-multipart (upload de arquivos)
# install fastapi e uvicorn, executar no terminal: pip install fastapi uvicorn
# para instalar o SQLAlchemy Utils, executar no terminal: pip install sqlalchemy-utils
# 2- para instalar o Alembic, executar no terminal: pip install alembic
# para inicializar o Alembic, executar no terminal: alembic init alembic
# 4- para criar uma nova migração, executar no terminal: alembic revision --autogenerate -m "nome_da_migração"
# 3- para migrar o banco de dados, executar no terminal: alembic upgrade head
# 5- para ver o histórico de migrações, executar no terminal: alembic history
# 6- para desfazer a última migração, executar no terminal: alembic downgrade -1
# 7- para desfazer todas as migrações, executar no terminal: alembic downgrade base