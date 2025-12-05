CREATE SCHEMA IF NOT EXISTS audit;

CREATE TYPE ordem_status AS ENUM ('ABERTA','PAUSADA','CANCELADA','EM ANDAMENTO','FINALIZADA');

CREATE TABLE IF NOT EXISTS cliente (
  id            BIGSERIAL PRIMARY KEY,
  nome          TEXT NOT NULL,
  telefone      TEXT NOT NULL,
  email         TEXT NOT NULL,
  ativo         BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS cliente_telefone_uq ON cliente(telefone);
CREATE UNIQUE INDEX IF NOT EXISTS cliente_email_uq ON cliente(email);

CREATE TABLE IF NOT EXISTS servico (
  id            BIGSERIAL PRIMARY KEY,
  descricao     TEXT NOT NULL,
  valor_base    NUMERIC(12,2) NOT NULL CHECK (valor_base >= 0),
  ativo         BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS funcionario (
  id            BIGSERIAL PRIMARY KEY,
  nome          TEXT NOT NULL,
  cargo         TEXT,
  ativo         BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ordem_servico (
  id              BIGSERIAL PRIMARY KEY,
  cliente_id      BIGINT NOT NULL,
  data_abertura   TIMESTAMPTZ NOT NULL DEFAULT now(),
  status          ordem_status NOT NULL DEFAULT 'ABERTA',
  ativo           BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT fk_ordem_servico_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_ordem_servico_cliente_id ON ordem_servico(cliente_id);

CREATE TABLE IF NOT EXISTS item_servico (
  id                  BIGSERIAL PRIMARY KEY,
  ordem_servico_id    BIGINT NOT NULL,
  servico_id          BIGINT NOT NULL,
  valor               NUMERIC(12,2) NOT NULL CHECK (valor >= 0),
  ativo               BOOLEAN NOT NULL DEFAULT TRUE,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT fk_item_servico_ordem FOREIGN KEY (ordem_servico_id) REFERENCES ordem_servico(id) ON DELETE CASCADE,
  CONSTRAINT fk_item_servico_servico FOREIGN KEY (servico_id) REFERENCES servico(id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX IF NOT EXISTS item_servico_ordem_servico_servico_uq ON item_servico(ordem_servico_id, servico_id);
CREATE INDEX IF NOT EXISTS idx_item_servico_ordem_id ON item_servico(ordem_servico_id);
CREATE INDEX IF NOT EXISTS idx_item_servico_servico_id ON item_servico(servico_id);

CREATE TABLE IF NOT EXISTS audit.cliente_audit (
  id            BIGSERIAL PRIMARY KEY,
  operation     TEXT NOT NULL,
  operation_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  performed_by  TEXT,
  old_data      JSONB,
  new_data      JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_cliente_operation_ts ON audit.cliente_audit(operation_ts);

CREATE TABLE IF NOT EXISTS audit.servico_audit (
  id            BIGSERIAL PRIMARY KEY,
  operation     TEXT NOT NULL,
  operation_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  performed_by  TEXT,
  old_data      JSONB,
  new_data      JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_servico_operation_ts ON audit.servico_audit(operation_ts);

CREATE TABLE IF NOT EXISTS audit.funcionario_audit (
  id            BIGSERIAL PRIMARY KEY,
  operation     TEXT NOT NULL,
  operation_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  performed_by  TEXT,
  old_data      JSONB,
  new_data      JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_funcionario_operation_ts ON audit.funcionario_audit(operation_ts);

CREATE TABLE IF NOT EXISTS audit.ordem_servico_audit (
  id            BIGSERIAL PRIMARY KEY,
  operation     TEXT NOT NULL,
  operation_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  performed_by  TEXT,
  old_data      JSONB,
  new_data      JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_ordem_servico_operation_ts ON audit.ordem_servico_audit(operation_ts);

CREATE TABLE IF NOT EXISTS audit.item_servico_audit (
  id            BIGSERIAL PRIMARY KEY,
  operation     TEXT NOT NULL,
  operation_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  performed_by  TEXT,
  old_data      JSONB,
  new_data      JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_item_servico_operation_ts ON audit.item_servico_audit(operation_ts);

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_set_updated_at_cliente
BEFORE UPDATE ON cliente
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_set_updated_at_servico
BEFORE UPDATE ON servico
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_set_updated_at_funcionario
BEFORE UPDATE ON funcionario
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_set_updated_at_ordem_servico
BEFORE UPDATE ON ordem_servico
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_set_updated_at_item_servico
BEFORE UPDATE ON item_servico
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

CREATE OR REPLACE FUNCTION audit.audit_row_to_audit()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  v_old jsonb;
  v_new jsonb;
  v_operation text;
  v_audit_table text;
BEGIN
  IF TG_OP = 'INSERT' THEN
    v_old := NULL;
    v_new := row_to_json(NEW)::jsonb;
    v_operation := 'INSERT';
  ELSIF TG_OP = 'UPDATE' THEN
    v_old := row_to_json(OLD)::jsonb;
    v_new := row_to_json(NEW)::jsonb;
    v_operation := 'UPDATE';
  ELSIF TG_OP = 'DELETE' THEN
    v_old := row_to_json(OLD)::jsonb;
    v_new := NULL;
    v_operation := 'DELETE';
  END IF;

  v_audit_table := format('audit.%I_audit', TG_TABLE_NAME);

  EXECUTE format(
    'INSERT INTO %s (operation, operation_ts, performed_by, old_data, new_data) VALUES ($1, now(), $2, $3, $4)',
    v_audit_table
  )
  USING v_operation, current_user, v_old, v_new;

  IF TG_OP = 'DELETE' THEN
    RETURN OLD;
  ELSE
    RETURN NEW;
  END IF;
END;
$$;

CREATE TRIGGER trg_audit_cliente
AFTER INSERT OR UPDATE OR DELETE ON cliente
FOR EACH ROW
EXECUTE FUNCTION audit.audit_row_to_audit();

CREATE TRIGGER trg_audit_servico
AFTER INSERT OR UPDATE OR DELETE ON servico
FOR EACH ROW
EXECUTE FUNCTION audit.audit_row_to_audit();

CREATE TRIGGER trg_audit_funcionario
AFTER INSERT OR UPDATE OR DELETE ON funcionario
FOR EACH ROW
EXECUTE FUNCTION audit.audit_row_to_audit();

CREATE TRIGGER trg_audit_ordem_servico
AFTER INSERT OR UPDATE OR DELETE ON ordem_servico
FOR EACH ROW
EXECUTE FUNCTION audit.audit_row_to_audit();

CREATE TRIGGER trg_audit_item_servico
AFTER INSERT OR UPDATE OR DELETE ON item_servico
FOR EACH ROW
EXECUTE FUNCTION audit.audit_row_to_audit();