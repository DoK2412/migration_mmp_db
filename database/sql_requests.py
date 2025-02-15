
NEW_USER = '''
-- добавление нового пользователя
INSERT INTO users
    (user_id, first_name, role, activity, creation_date, tg_id)
VALUES 
    ($1, $2, $3, $4, $5, $6) 
'''

ADD_TYPE = '''
-- добавление типов операций
INSERT INTO operations_type (type) VALUES ($1) 
'''

ADD_ROLE = '''
-- добавление роли пользователя
INSERT INTO user_role (type) VALUES ($1) 
'''

NEW_WALLET = '''
-- добавленеие кошелька пользователя
INSERT INTO wallets
    (wallet_id, holder_id, name, amount, currency, active, pinned, pin_on_main, verified, description, status, show, color)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) 
'''

TYPE_ID = '''
-- получение типа операции
SELECT id FROM operations_type WHERE type = $1

'''
USER_ID_NEW = '''
-- получеение id пользователя
SELECT id FROM users WHERE first_name = $1
'''

USER_ID = '''
-- получеение id пользователя
SELECT id FROM users WHERE user_id = $1
'''

WALLET_ID = '''
-- получение id кошелька
SELECT id FROM wallets WHERE wallet_id = $1

'''

ADD_FROM_WALLETS = '''
-- добавление операции для кошелька
INSERT INTO from_wallets
    (before, amount, after, wallet_id, creature_date, currency)
VALUES 
    ($1, $2, $3, $4, $5, $6) RETURNING id
'''

ADD_TO_WALLETS = '''
-- добавление операции из кошелька
INSERT INTO to_wallets
    (before, amount, after, wallet_id, creature_date, currency)
VALUES 
    ($1, $2, $3, $4, $5, $6) RETURNING id
'''

ADD_OPERATION = '''
-- добавление общей операции 
INSERT INTO operations
    (operations_id, type_id, creature_date, description, user_id, from_wallets_id, to_wallets_id, groups)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7, $8)
'''

ADD_OLD = '''
-- добавление корректировки до начала
INSERT INTO adjustment_old
    (wallet_id, amount, verified, description, status, color, creature_date, name, currency)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id
'''

ADD_NEW = '''
-- добавление корректировки до начала
INSERT INTO adjustment_new
    (wallet_id, amount, verified, description, status, color, creature_date, name, currency)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id
'''

ADD_OPERATION_KOR = '''
-- добавление общей операции корректировки
INSERT INTO operations
    (operations_id, type_id, creature_date, description, user_id, adjustment_oll_id, adjustment_new_id, groups, from_wallets_id, to_wallets_id)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
'''

ADD_WRITE_BALANSE = '''
-- добавление баланса записи
INSERT INTO write_balance
    (date, wallet_id, amount, currency, user_id)
VALUES
    ($1, $2, $3, $4, $5) RETURNING id
'''

ADD_OPERATION_WRITE = '''
-- добавление общей операции баланса записи
INSERT INTO operations
    (operations_id, type_id, creature_date, user_id, write_id)
VALUES 
    ($1, $2, $3, $4, $5)
'''
