CREATE TABLE IF NOT EXISTS public.oracle_leads (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    session_id TEXT UNIQUE NOT NULL,
    niche TEXT,
    bottleneck TEXT,
    scale_potential TEXT,
    qualification_score INTEGER DEFAULT 0,
    is_qualified BOOLEAN DEFAULT FALSE,
    raw_analysis JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Habilitar RLS
ALTER TABLE public.oracle_leads ENABLE ROW LEVEL SECURITY;

-- Política de acesso total (para fins de desenvolvimento/admin)
CREATE POLICY "Allow all access to oracle_leads" ON public.oracle_leads
    FOR ALL USING (true) WITH CHECK (true);
;
