-- ALTER TABLE transactions
-- ADD COLUMN user_id INT,
-- ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- select * from transactions
-- select * from users
-- select * from accounts

--  DROP TABLE transactions



-- CREATE TABLE transactions (
-- transactions_id SERIAL PRIMARY KEY,
-- user_id INT,
-- from_account_id INT,
-- to_account_id INT,
-- amount DECIMAL(10, 2) NOT NULL,
-- trasaction_type VARCHAR(255) NOT NULL,
-- description VARCHAR(255),
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (from_account_id) REFERENCES accounts(account_id),
-- FOREIGN KEY (to_account_id) REFERENCES accounts(account_id),
-- FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
-- );

-- INSERT INTO transactions 
--     (user_id, from_account_id, to_account_id, amount, trasaction_type, description)
-- VALUES
--     (2, 3, 2, 1500000.00, 'Transfer', 'Transfer antar rekening');

-- INSERT INTO transactions 
--     (user_id, from_account_id, to_account_id, amount, trasaction_type, description)
-- VALUES
--     (1, 1, 2, 1500000.00, 'Transfer', 'Transfer antar rekening');

-- ALTER TABLE transactions 
-- RENAME COLUMN trasaction_type TO transaction_type;


-- SELECT 
--     t.transactions_id,
--     t.user_id,
--     t.from_account_id,
--     u_from.full_name AS from_user,
--     t.to_account_id,
--     u_to.full_name AS to_user,
--     t.amount,
--     t.transaction_type,
--     t.description
-- FROM transactions t
-- LEFT JOIN accounts a_from ON t.from_account_id = a_from.account_id
-- LEFT JOIN users u_from ON a_from.user_id = u_from.user_id
-- LEFT JOIN accounts a_to ON t.to_account_id = a_to.account_id
-- LEFT JOIN users u_to ON a_to.user_id = u_to.user_id
-- WHERE t.user_id = 1
-- AND t.amount >= 100000.00;



-- CREATE TABLE users (
-- user_id VARCHAR (5) PRIMARY KEY,
-- username VARCHAR (255) UNIQUE NOT NULL,
-- user_email VARCHAR(255) UNIQUE NOT NULL,
-- user_password VARCHAR (20) NOT NULL,
-- first_name VARCHAR (255) NOT NULL,
-- last_name VARCHAR (255) NOT NULL,
-- full_name VARCHAR (255),
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- )

-- select * from users
-- select * from accounts

-- CREATE TABLE accounts (
-- account_id VARCHAR (5) PRIMARY KEY,
-- user_id VARCHAR NOT NULL,
-- account_type VARCHAR (255) NOT NULL,
-- account_number VARCHAR (255) UNIQUE NOT NULL,
-- balance DECIMAL (10,2) DEFAULT 0.00,
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
-- );

-- CREATE TABLE transactions (
-- transactions_id SERIAL PRIMARY KEY,
-- user_id VARCHAR,
-- from_account_id VARCHAR,
-- to_account_id VARCHAR,
-- amount DECIMAL(10, 2) NOT NULL,
-- trasaction_type VARCHAR(255) NOT NULL,
-- description VARCHAR(255),
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (from_account_id) REFERENCES accounts(account_id),
-- FOREIGN KEY (to_account_id) REFERENCES accounts(account_id),
-- FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
-- );

-- -- drop table transactions


-- CREATE TABLE transactions (
--     transaction_id VARCHAR(20) PRIMARY KEY,
--     user_id VARCHAR(5) REFERENCES users(user_id) ON DELETE CASCADE,
--     from_account_id VARCHAR(5) REFERENCES accounts(account_id),
--     to_account_id VARCHAR(5) REFERENCES accounts(account_id),
--     amount DECIMAL(10,2) NOT NULL,
--     transaction_type VARCHAR(20) NOT NULL,
--     balance_before DECIMAL(10,2) NOT NULL,
--     balance_after DECIMAL(10,2) NOT NULL,
--     description VARCHAR(255),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- select * from transactions





