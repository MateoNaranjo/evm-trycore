# Changelog

## [1.0.0] - 2026-11-13

Primera versión de EVM Tracker.

### Backend
- API REST para crear, consultar, editar y eliminar proyectos y actividades.
- Cálculo de indicadores de Valor Ganado (PV, EV, CV, SV, CPI, SPI, EAC, VAC) por actividad y consolidado por proyecto, ponderado por presupuesto.
- Interpretación de CPI y SPI: bajo/en/sobre presupuesto y adelantado/a tiempo/atrasado.
- Manejo de casos borde: índices `null` con estado `NOT_AVAILABLE` cuando AC, PV o CPI son cero.
- Documentación OpenAPI en `/swagger-ui` y `/api-docs`.
- Pruebas unitarias del cálculo EVM y pruebas de integración de cada endpoint (cobertura de la capa de negocio: 100 %).

### Frontend
- Dashboard para seleccionar, crear y eliminar proyectos.
- Estado general del proyecto y semáforo de CPI y SPI con explicación en lenguaje simple.
- Tarjetas con los indicadores consolidados.
- Gráfica comparativa de PV, EV y AC por actividad.
- Tabla de actividades con sus indicadores y formulario para crearlas y editarlas.

### Base de datos
- Script de inicialización `db/init.sql` y datos de demostración `db/seed.sql`.
- `docker-compose.yml` para levantar PostgreSQL con el esquema y los datos de demostración.
