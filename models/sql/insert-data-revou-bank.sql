---------- USERS ----------


SELECT * FROM users

INSERT INTO users 
    (username, user_email, user_password, first_name, last_name, full_name)
VALUES
    ('aizarfarhan25', 'aizar@gmail.com', 'password123', 'Aizar', 'Farhan', 'Aizar Farhan'),
    ('yanto_gantenk', 'yanktonk@gmail.com', 'password123', 'Yanto', 'Suranto', 'Yanto Suranto'),
    ('natdcoco', 'natadcoco@gmail.com', 'jambul123', 'Nata', 'Decoco', 'Nata Decoco');


---------- ACCOUNTS ----------


SELECT * FROM accounts

-- buat multiple account from 1 user
INSERT INTO accounts
	(user_id, account_type, account_number, balance)
VALUES
    (1, 'Tabungan', 'ACC001', 1000000.00),
    (1, 'Giro', 'ACC002', 5000000.00);

-- buat single account from 1 user
INSERT INTO accounts 
    (user_id, account_type, account_number)
VALUES
    (2, 'Tabungan', 'ACC003'); -- Saldo default 0.00


---------- TRANSACTIONS ----------

SELECT * FROM transactions

-- deposit
INSERT INTO transactions 
    (to_account_id, amount, trasaction_type, description)
VALUES
    (1, 2000000.00, 'Setoran', 'Setor tunai');

-- transfer
INSERT INTO transactions 
    (from_account_id, to_account_id, amount, trasaction_type, description)
VALUES
    (1, 2, 1500000.00, 'Transfer', 'Transfer antar rekening');

-- withdraw
INSERT INTO transactions 
    (from_account_id, amount, trasaction_type, description)
VALUES
    (2, 500000.00, 'Penarikan', 'Tarik tunai di ATM');


