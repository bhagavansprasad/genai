#!/bin/bash

# Define base project directory
PROJECT_ROOT="servers"

# Define subdirectories
mkdir -p "$PROJECT_ROOT/stock_details/app/routers"
mkdir -p "$PROJECT_ROOT/company_details/app/routers"
mkdir -p "$PROJECT_ROOT/news_service/app/routers"
mkdir -p "$PROJECT_ROOT/shared"

# Create directories
echo "Creating project directory structure..."
for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"
done

# Create common files
echo "Creating common files..."

# Shared module for database connection
cat > "$PROJECT_ROOT/shared/db_connection.py" <<EOL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@postgres_db/stock_data")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
EOL

# Create environment file
cat > "$PROJECT_ROOT/.env" <<EOL
DATABASE_URL=postgresql://bhagavan:jnjnuh@postgres_db/stock_data
EOL

# Create README file
cat > "$PROJECT_ROOT/README.md" <<EOL
# FastAPI Microservices for Stock Data

## Services:
1. **Stock Details Service** (Runs on Port 8001)
2. **Company Financials Service** (Runs on Port 8002)
3. **News Service** (Runs on Port 8003)

## How to Run
1. Install Docker & Docker Compose
2. Run \`docker-compose up --build\`
EOL

# Create Docker Compose File
cat > "$PROJECT_ROOT/docker-compose.yml" <<EOL
version: '3.8'

services:
  stock-service:
    build: ./stock_details
    ports:
      - "8001:8000"
    depends_on:
      - postgres_db
    env_file:
      - .env

  company-service:
    build: ./company_details
    ports:
      - "8002:8000"
    depends_on:
      - postgres_db
    env_file:
      - .env

  news-service:
    build: ./news_service
    ports:
      - "8003:8000"
    depends_on:
      - postgres_db
    env_file:
      - .env

  postgres_db:
    image: postgres:latest
    container_name: postgres_container
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: stock_data
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
EOL

# Generate base FastAPI files for each server
for SERVICE in "stock_details" "company_details" "news_service"; do
    cat > "$PROJECT_ROOT/$SERVICE/app/main.py" <<EOL
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to $SERVICE"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOL

    cat > "$PROJECT_ROOT/$SERVICE/app/models.py" <<EOL
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    revenue = Column(DECIMAL(15,2), nullable=False)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    headline = Column(String, nullable=False)
EOL

    cat > "$PROJECT_ROOT/$SERVICE/app/schemas.py" <<EOL
from pydantic import BaseModel

class StockSchema(BaseModel):
    symbol: str
    company_name: str
    price: float

class CompanySchema(BaseModel):
    symbol: str
    revenue: float

class NewsSchema(BaseModel):
    symbol: str
    headline: str
EOL

    cat > "$PROJECT_ROOT/$SERVICE/app/database.py" <<EOL
from sqlalchemy.orm import Session
from shared.db_connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOL

    cat > "$PROJECT_ROOT/$SERVICE/Dockerfile" <<EOL
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary pydantic
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

    cat > "$PROJECT_ROOT/$SERVICE/requirements.txt" <<EOL
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
EOL
done

echo "Project structure created successfully!"

