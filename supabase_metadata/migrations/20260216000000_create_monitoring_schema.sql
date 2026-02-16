-- Migration: Create Monitored Wallets Schema
-- Target: safetransfer schema

CREATE TABLE IF NOT EXISTS safetransfer.monitored_wallets (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    telegram_id TEXT NOT NULL, -- ID do usuário no Telegram para notificações
    address TEXT NOT NULL,
    network TEXT NOT NULL DEFAULT 'ETH',
    is_active BOOLEAN DEFAULT true,
    last_scan TIMESTAMP WITH TIME ZONE DEFAULT now(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE(telegram_id, address, network)
);

-- Habilitar RLS por segurança
ALTER TABLE safetransfer.monitored_wallets ENABLE ROW LEVEL SECURITY;

-- Política simples: permitir leitura/escrita para anon/service_role (ajustar se necessário)
CREATE POLICY "Allow all for now" ON safetransfer.monitored_wallets
    FOR ALL USING (true) WITH CHECK (true);
