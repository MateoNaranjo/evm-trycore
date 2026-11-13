# EVM Tracker

Herramienta interna para que los líderes de proyecto registren el avance de sus actividades y vean, en tiempo real, si el proyecto va bien o mal en cronograma y presupuesto usando la metodología de Valor Ganado (Earned Value Management).

La arquitectura, las decisiones técnicas y los conceptos usados se explican en [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md).

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12+ · FastAPI · SQLAlchemy 2 |
| Base de datos | PostgreSQL 17 |
| Frontend | React 19 · Vite 6 · Recharts |
| Pruebas | pytest · pytest-cov |
| Linters | Ruff (backend) · ESLint (frontend) |

## Estructura

```
backend/
  app/
    api/          Endpoints REST y manejo de errores (sin lógica de negocio)
    schemas/      Contratos de request y response (Pydantic)
    services/     Casos de uso: orquestan repositorio y dominio
    domain/       Cálculo EVM puro, sin dependencias de framework
    persistence/  Modelos ORM y repositorio
    core/         Configuración y conexión a base de datos
  tests/
db/init.sql     Script de inicialización de la base de datos
db/seed.sql     Datos de demostración (1 proyecto, 4 actividades)
frontend/
  src/
    api/          Cliente HTTP del backend
    hooks/        Carga de datos
    components/   Selector, indicadores, semáforo, gráfica, tabla y formulario
    utils/        Formato e interpretación de indicadores
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
psql -U postgres -d evm_db -f db/seed.sql     # opcional: datos de demostración
```

**Opción B — Docker**

```bash
docker compose up -d
```

El contenedor ejecuta `db/init.sql` y `db/seed.sql` automáticamente la primera vez.

El seed es idempotente: si el proyecto de demostración ya existe, no inserta nada.

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

## API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/projects` | Lista proyectos con sus indicadores consolidados |
| POST | `/api/projects` | Crea un proyecto |
| GET | `/api/projects/{id}` | Proyecto con actividades, indicadores por actividad y consolidado |
| PUT | `/api/projects/{id}` | Edita un proyecto |
| DELETE | `/api/projects/{id}` | Elimina un proyecto y sus actividades |
| POST | `/api/projects/{id}/activities` | Crea una actividad |
| PUT | `/api/projects/{id}/activities/{activityId}` | Edita una actividad |
| DELETE | `/api/projects/{id}/activities/{activityId}` | Elimina una actividad |

Errores: `404` si el recurso no existe, `422` si los datos no cumplen las validaciones.

## Cálculo EVM

| Indicador | Fórmula |
|---|---|
| PV | % planificado × BAC |
| EV | % completado × BAC |
| CV | EV − AC |
| SV | EV − PV |
| CPI | EV / AC |
| SPI | EV / PV |
| EAC | BAC / CPI |
| VAC | BAC − EAC |

- **Consolidado del proyecto:** se suman BAC, PV, EV y AC de las actividades y luego se aplican las fórmulas. No se promedian los índices, para que cada actividad pese según su presupuesto.
- **Divisiones no definidas:** si AC, PV o CPI son cero, el índice correspondiente (y EAC/VAC cuando aplica) se devuelve como `null` con estado `NOT_AVAILABLE`.
- **Redondeo:** se calcula con precisión decimal completa y se redondea al final (2 decimales para dinero, 4 para índices).

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
