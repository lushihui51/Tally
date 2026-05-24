DROP TABLE IF EXISTS spending_secondary_category;
DROP TABLE IF EXISTS split_arrangement;
DROP TABLE IF EXISTS beneficiaries_individual;
DROP TABLE IF EXISTS spenders_individual;
DROP TABLE IF EXISTS spending;
DROP TABLE IF EXISTS secondary_category;
DROP TABLE IF EXISTS primary_category;
DROP TABLE IF EXISTS individual;

CREATE TABLE individual (
    individual_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE primary_category (
    primary_category_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE secondary_category (
    secondary_category_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE spending (
    spending_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    aggregated BOOLEAN NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    spending_date DATE NOT NULL,
    essential BOOLEAN NOT NULL,
    settled BOOLEAN NOT NULL,
    primary_category_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (primary_category_name) REFERENCES primary_category(primary_category_name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    store_name VARCHAR(50) NOT NULL,
    store_location VARCHAR(255) NOT NULL
);

CREATE TABLE spenders_individual (
    spending_id INTEGER,
    individual_name VARCHAR(50),
    contribution DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (spending_id) REFERENCES spending(spending_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (individual_name) REFERENCES individual(individual_name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    PRIMARY KEY (spending_id, individual_name)
);

CREATE TABLE beneficiaries_individual (
    spending_id INTEGER,
    individual_name VARCHAR(50),
    FOREIGN KEY (spending_id) REFERENCES spending(spending_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (individual_name) REFERENCES individual(individual_name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    PRIMARY KEY (spending_id, individual_name)
);

CREATE TABLE split_arrangement (
    individual_a VARCHAR(50),
    individual_b VARCHAR(50),
    a_proportion DECIMAL(10, 2) NOT NULL,
    categories JSONB NOT NULL,
    FOREIGN KEY (individual_a) REFERENCES individual(individual_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (individual_b) REFERENCES individual(individual_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (individual_a, individual_b),
    CONSTRAINT check_different_individuals CHECK (individual_a != individual_b),
    CONSTRAINT check_ordered_pair CHECK (individual_a < individual_b)
);

CREATE TABLE spending_secondary_category (
    spending_id INTEGER,
    secondary_category_name VARCHAR(50),
    FOREIGN KEY (spending_id) REFERENCES spending(spending_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (secondary_category_name) REFERENCES secondary_category(secondary_category_name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    PRIMARY KEY (spending_id, secondary_category_name)
);