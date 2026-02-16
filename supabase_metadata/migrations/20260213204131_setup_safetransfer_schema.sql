-- 1. Criar o Schema dedicado
CREATE SCHEMA IF NOT EXISTS safetransfer;

-- 2. Habilitar extensões no schema public (padrão)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 3. Tabela de Ativos
CREATE TABLE safetransfer.assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabela de Plataformas
CREATE TABLE safetransfer.platforms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('CEX', 'WALLET')),
    icon_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Network Registry
CREATE TABLE safetransfer.network_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES safetransfer.assets(id) ON DELETE CASCADE,
    origin_id UUID REFERENCES safetransfer.platforms(id) ON DELETE CASCADE,
    network_name TEXT NOT NULL,
    destination_id UUID REFERENCES safetransfer.platforms(id) ON DELETE CASCADE,
    is_supported BOOLEAN DEFAULT TRUE,
    risk_level TEXT CHECK (risk_level IN ('SAFE', 'CAUTION', 'DANGEROUS')) DEFAULT 'SAFE',
    technical_note TEXT,
    human_warning TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Logs de Verificação
CREATE TABLE safetransfer.verification_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    query_payload JSONB NOT NULL,
    status TEXT NOT NULL,
    response_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices de Performance
CREATE INDEX idx_safetransfer_registry_lookup ON safetransfer.network_registry (asset_id, origin_id, network_name, destination_id);
CREATE INDEX idx_safetransfer_logs_created_at ON safetransfer.verification_logs USING BRIN (created_at);
;
