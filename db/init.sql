-- Script de inicialización de la base de datos EVM Tracker.
-- Los indicadores EVM (PV, EV, CV, SV, CPI, SPI, EAC, VAC) no se almacenan:
-- son datos derivados y se calculan al consultar.

CREATE TABLE IF NOT EXISTS projects (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL CHECK (char_length(trim(name)) > 0),
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS activities (
    id                   SERIAL PRIMARY KEY,
    project_id           INTEGER NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
    name                 VARCHAR(150) NOT NULL CHECK (char_length(trim(name)) > 0),
    budget_at_completion NUMERIC(14, 2) NOT NULL CHECK (budget_at_completion > 0),
    planned_percentage   NUMERIC(5, 2) NOT NULL CHECK (planned_percentage BETWEEN 0 AND 100),
    actual_percentage    NUMERIC(5, 2) NOT NULL CHECK (actual_percentage BETWEEN 0 AND 100),
    actual_cost          NUMERIC(14, 2) NOT NULL CHECK (actual_cost >= 0),
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_activities_project_id ON activities (project_id);
