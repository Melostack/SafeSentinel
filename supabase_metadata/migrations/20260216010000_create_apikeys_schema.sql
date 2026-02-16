-- Migration: Create API Keys Schema for B2B
-- Target: safetransfer schema

CREATE TABLE IF NOT EXISTS safetransfer.api_keys (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    key_prefix TEXT NOT NULL, -- Primeiros 8 caracteres para identificação visual (ex: sk_live_...)
    key_hash TEXT NOT NULL UNIQUE, -- Hash SHA-256 da chave completa
    owner_name TEXT NOT NULL,
    plan_type TEXT DEFAULT 'FREE', -- FREE, PRO, ENTERPRISE
    requests_limit INTEGER DEFAULT 100,
    requests_used INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_used TIMESTAMP WITH TIME ZONE
);

-- Habilitar RLS
ALTER TABLE safetransfer.api_keys ENABLE ROW LEVEL SECURITY;

-- Política de acesso: Apenas o service_role ou anon (via API autenticada internamente)
CREATE POLICY "Internal service access" ON safetransfer.api_keys
    FOR ALL USING (true) WITH CHECK (true);
