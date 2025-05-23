-- Table: athlete_users
CREATE TABLE IF NOT EXISTS athlete_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash BYTEA NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: readiness_assessment
CREATE TABLE IF NOT EXISTS readiness_assessment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES athlete_users(id),
    date DATE NOT NULL,
    sleep_quality INTEGER,
    sleep_duration INTEGER,
    stress_level INTEGER,
    muscle_soreness INTEGER,
    energy_level INTEGER,
    motivation INTEGER,
    nutrition_quality INTEGER,
    hydration INTEGER,
    readiness_score FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: training_assessment
CREATE TABLE IF NOT EXISTS training_assessment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES athlete_users(id),
    date DATE NOT NULL,
    training_load FLOAT,
    training_duration INTEGER,
    rpe INTEGER,
    intensity_zone INTEGER,
    training_type VARCHAR(255),
    fatigue_level INTEGER,
    performance_feeling INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: psychological_assessment
CREATE TABLE IF NOT EXISTS psychological_assessment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES athlete_users(id),
    date DATE NOT NULL,
    depression_score INTEGER,
    anxiety_score INTEGER,
    stress_score INTEGER,
    intrinsic_motivation INTEGER,
    extrinsic_motivation INTEGER,
    amotivation INTEGER,
    flow_score INTEGER,
    confidence_level INTEGER,
    focus_ability INTEGER,
    emotional_state INTEGER,
    pre_competition_anxiety INTEGER,
    satisfaction_with_training INTEGER,
    team_cohesion INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: training_session
CREATE TABLE IF NOT EXISTS training_session (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES athlete_users(id),
    date DATE NOT NULL,
    title VARCHAR(255),
    description TEXT,
    training_type VARCHAR(255),
    planned_duration INTEGER,
    actual_duration INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: goal
CREATE TABLE IF NOT EXISTS goal (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES athlete_users(id),
    title VARCHAR(255),
    description TEXT,
    target_date DATE,
    metric_type VARCHAR(255),
    target_value FLOAT,
    current_value FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
