CREATE TABLE customers (
    id UUID PRIMARY KEY,
    source_id INT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT
);