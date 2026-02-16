-- Garantir extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Oracle Memory: Conversations History
CREATE TABLE IF NOT EXISTS oracle_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    role TEXT CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for session performance
CREATE INDEX IF NOT EXISTS idx_oracle_memory_session_id ON oracle_memory(session_id);

-- Oracle Knowledge: RAG Base
CREATE TABLE IF NOT EXISTS oracle_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    embedding VECTOR(768), -- Adjusted for Gemini embeddings (768 dimensions)
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Oracle Prompts: Versioning for System Prompts
CREATE TABLE IF NOT EXISTS oracle_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS (Row Level Security)
ALTER TABLE oracle_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE oracle_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE oracle_prompts ENABLE ROW LEVEL SECURITY;

-- Políticas de RLS (usando DO blocks para evitar erro se já existirem)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow anon insert memory') THEN
        CREATE POLICY "Allow anon insert memory" ON oracle_memory FOR INSERT WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow anon read memory') THEN
        CREATE POLICY "Allow anon read memory" ON oracle_memory FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow anon read prompts') THEN
        CREATE POLICY "Allow anon read prompts" ON oracle_prompts FOR SELECT USING (is_active = true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow read knowledge') THEN
        CREATE POLICY "Allow read knowledge" ON oracle_knowledge FOR SELECT USING (true);
    END IF;
END $$;

-- Function for semantic search
CREATE OR REPLACE FUNCTION match_oracle_knowledge(
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    ok.id,
    ok.content,
    ok.metadata,
    1 - (ok.embedding <=> query_embedding) AS similarity
  FROM oracle_knowledge ok
  WHERE 1 - (ok.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;;
