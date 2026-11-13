# EVM Tracker

Herramienta interna para que los líderes de proyecto registren el avance de sus actividades y vean, en tiempo real, si el proyecto va bien o mal en cronograma y presupuesto usando la metodología de Valor Ganado (Earned Value Management).

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12+ · FastAPI · SQLAlchemy 2 |
| Base de datos | PostgreSQL 17 |
| Frontend | React 19 · Vite 6 |
| Pruebas | pytest · pytest-cov |
| Linters | Ruff (backend) · ESLint (frontend) |

## Estructura

```
backend/
  app/
    api/        Endpoints REST (sin lógica de negocio)
    services/   Casos de uso: orquestan repositorios y dominio
    domain/     Cálculo EVM puro, sin dependencias de framework
    core/       Configuración y conexión a base de datos
  tests/
db/init.sql     Script de inicialización de la base de datos
frontend/       Dashboard React
```

## Requisitos

- Python 3.12 o superior
- Node.js 20 o superior
- PostgreSQL 17 (instalado localmente o con Docker)

## Cómo correr el proyecto localmente

### 1. Base de datos

**Opción A — PostgreSQL instalado localmente**

```bash
psql -U postgres -c "CREATE DATABASE evm_db;"
psql -U postgres -d evm_db -f db/init.sql
```

**Opción B — Docker**

```bash
docker compose up -d
```

El contenedor ejecuta `db/init.sql` automáticamente la primera vez.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
pip install -r requirements-dev.txt
cp .env.example .env          # ajustar usuario y contraseña de PostgreSQL
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api
- Swagger UI: http://localhost:8000/swagger-ui
- Especificación OpenAPI: http://localhost:8000/api-docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:5173

## Pruebas y calidad

```bash
cd backend
pytest --cov                  # falla si la cobertura de la capa de negocio es menor a 80 %
ruff check .
```

```bash
cd frontend
npm run lint
```

## Flujo de trabajo (Gitflow)

- `main`: producción
- `develop`: integración
- `feature/*`: una rama por funcionalidad, integrada a `develop` mediante Pull Request
- `release/*`: preparación de versión antes de integrar a `main`

## Proceso con IA

Ver [AI_PROCESS.md](AI_PROCESS.md).
