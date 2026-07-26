CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    filename VARCHAR(255) NOT NULL UNIQUE,

    filepath TEXT NOT NULL,

    file_type VARCHAR(20) NOT NULL,

    file_size BIGINT NOT NULL,

    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);