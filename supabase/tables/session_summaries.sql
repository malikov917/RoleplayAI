CREATE TABLE session_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL UNIQUE,
    performance_score INTEGER,
    feedback_text TEXT,
    strengths TEXT,
    improvement_areas TEXT,
    key_insights TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);