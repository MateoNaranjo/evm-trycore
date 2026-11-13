-- Datos de demostración: un proyecto con cuatro actividades en situaciones distintas.
-- Es idempotente: si el proyecto ya existe, no inserta nada.
--
-- Valores esperados del consolidado (calculados a mano):
--   BAC 77.000 · PV 43.500 · EV 39.000 · AC 41.500 · CV -2.500 · SV -4.500
--   CPI 0,9398 (sobre presupuesto) · SPI 0,8966 (atrasado)
--   EAC 81.935,90 · VAC -4.935,90

WITH demo_project AS (
    INSERT INTO projects (name, description)
    SELECT 'Portal de autogestión de clientes',
           'Proyecto de demostración para el análisis de Valor Ganado'
    WHERE NOT EXISTS (
        SELECT 1 FROM projects WHERE name = 'Portal de autogestión de clientes'
    )
    RETURNING id
)
INSERT INTO activities (
    project_id, name, budget_at_completion, planned_percentage, actual_percentage, actual_cost
)
SELECT demo_project.id, activity.name, activity.budget, activity.planned, activity.actual, activity.cost
FROM demo_project
CROSS JOIN (
    VALUES
        -- Terminada, pero costó más de lo presupuestado: CPI 0,8889, SPI 1,0.
        ('Levantamiento de requerimientos', 12000.00, 100.00, 100.00, 13500.00),
        -- Atrasada y con sobrecosto: CPI 0,9, SPI 0,75.
        ('Desarrollo del backend', 40000.00, 60.00, 45.00, 20000.00),
        -- Adelantada y eficiente: CPI 1,125, SPI 1,2.
        ('Diseño de interfaz', 15000.00, 50.00, 60.00, 8000.00),
        -- Aún no inicia: sin costo ni avance, índices no calculables.
        ('Pruebas de aceptación', 10000.00, 0.00, 0.00, 0.00)
) AS activity (name, budget, planned, actual, cost);
