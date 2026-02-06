CREATE TABLE customers (
    id VARCHAR(36) PRIMARY KEY,
    source_id INT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT
);