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

-- -- Membuat Index untuk meningkatkan performa query
-- CREATE INDEX idx_accounts_user_id ON accounts(user_id);
-- CREATE INDEX idx_transactions_from_account ON transactions(from_account_id);
-- CREATE INDEX idx_transactions_to_account ON transactions(to_account_id);

-- -- Trigger untuk memperbarui kolom updated_at pada tabel users
-- CREATE OR REPLACE FUNCTION update_users_updated_at()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.updated_at = CURRENT_TIMESTAMP;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_update_users_timestamp
-- BEFORE UPDATE ON users
-- FOR EACH ROW
-- EXECUTE FUNCTION update_users_updated_at();

-- -- Trigger untuk memperbarui kolom updated_at pada tabel accounts
-- CREATE OR REPLACE FUNCTION update_accounts_updated_at()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.updated_at = CURRENT_TIMESTAMP;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_update_accounts_timestamp
-- BEFORE UPDATE ON accounts
-- FOR EACH ROW
-- EXECUTE FUNCTION update_accounts_updated_at();

-- -- Trigger untuk memperbarui kolom updated_at pada tabel transactions (jika diperlukan)
-- CREATE OR REPLACE FUNCTION update_transactions_updated_at()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.updated_at = CURRENT_TIMESTAMP;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_update_transactions_timestamp
-- BEFORE UPDATE ON transactions
-- FOR EACH ROW
-- EXECUTE FUNCTION update_transactions_updated_at();
