CREATE TABLE situations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    persona_script TEXT NOT NULL,
    difficulty_level VARCHAR(50) DEFAULT 'beginner',
    category VARCHAR(100) DEFAULT 'general',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);