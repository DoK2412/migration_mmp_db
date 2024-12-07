import json
import datetime

from database.connection import JobDb
import database.sql_requests as sql


async def create_user():
    try:
        filename = '/home/dok2412/PycharmProjects/migration_db_mmp/users.json'
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            type_operetion = ['Добавление кошелька', 'Корректировка', 'Продажа', 'Перевод', 'Расход', 'Покупка', 'Перенос', 'Удаление кошелька', 'Проверенный продажа', 'Проверенный покупка', 'Обмен', 'Хавала продажа', 'Конвертация', 'P2P покупка', 'Хавала покупка', 'P2P продажа', 'Зачисление', 'write_balance', 'Аванс']
            user_role = ['Admin', 'Minor']
            async with JobDb() as pool:
                for type in type_operetion:
                    await pool.fetchval(sql.ADD_TYPE, type)
                for role in user_role:
                    await pool.fetchval(sql.ADD_ROLE, role)
                for key, value in data.items():
                    if value['role'] == "Admin":
                        role = 1
                    else:
                        role = 2
                    date = datetime.datetime.now()
                    await pool.fetchrow(sql.NEW_USER, value['id'], value['first_name'], role, True, date, str(value['tg_id']))
        return "Пользователи успешно перенесены"
    except Exception as exc:
        return f"При переносе данных произошла ошибка {exc}"


async def create_wallet():
    try:
        filename = '/home/dok2412/PycharmProjects/migration_db_mmp/wallets.json'
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            async with JobDb() as pool:
                for key in data:
                    user_id = await pool.fetchval(sql.USER_ID_NEW, key['holder'])
                    await pool.fetchrow(sql.NEW_WALLET, key['id'], user_id, key['name'], key['amount'],
                                        key['currency'], key['active'], key['pinned'], key['pin_on_main'],
                                        key['verified'], key['description'], key['status'], key['show'],
                                        key['color'])
        return "Кошельки успешно перенесены"
    except Exception as exc:
        return f"При переносе данных произошла ошибка {exc}"


async def create_operation():
    try:

        filename = '/home/dok2412/PycharmProjects/migration_db_mmp/operations.json'

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for value in data:
                async with JobDb() as pool:

                    if value['type'] in ['Добавление кошелька', 'Удаление кошелька']:
                        continue
                    elif value['type'] == "write_balance":
                        type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                        user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                        wallet_id = await pool.fetchval(sql.WALLET_ID, value['wallet_id'])
                        write_id = await pool.fetchval(sql.ADD_WRITE_BALANSE, value['date'], wallet_id, value['amount'], value['currency'])
                        await pool.fetchval(sql.ADD_OPERATION_WRITE, value['id'], type_id, value['date'], user_id, write_id)
                    elif value['type'] == "Корректировка":
                        type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                        user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                        if value.get('old') and len(value['old']) > 0:
                            if value['old']['name'] == "wal1":
                                continue
                            else:
                                wallet_id = await pool.fetchval(sql.WALLET_ID, value['old']['id'])
                                date = datetime.datetime.now()
                                old_id = await pool.fetchval(sql.ADD_OLD, wallet_id, value['old']['amount'], value['old']['verified'], value['old']['description'], value['old']['status'], value['old']['color'], date)
                        else:
                            old_id = None

                        if value.get('new') and len(value['new']) > 0:
                            if value['new']['name'] == "wal1":
                                continue
                            else:
                                wallet_id = await pool.fetchval(sql.WALLET_ID, value['new']['id'])
                                date = datetime.datetime.now()
                                new_id = await pool.fetchval(sql.ADD_NEW, wallet_id, value['new']['amount'], value['new']['verified'], value['new']['description'], value['new']['status'], value['new']['color'], date)
                        else:
                            new_id = None

                        await pool.fetchval(sql.ADD_OPERATION_KOR, value['id'], type_id, value['date'], value['description'], user_id, old_id, new_id, value['group'])

                    else:
                        type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                        user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                        if value.get('from_wallets') and len(value['from_wallets']) > 0:
                            wallet_id = await pool.fetchval(sql.WALLET_ID, value['from_wallets'][0]['id'])
                            from_wallets_id = await pool.fetchval(sql.ADD_FROM_WALLETS,
                                                                  value['from_wallets'][0]['before'],
                                                                  value['from_wallets'][0]['amount'],
                                                                  value['from_wallets'][0]['after'], wallet_id,
                                                                  value['date'], value['from_wallets'][0]['currency'])
                        else:
                            from_wallets_id = None
                        if value.get('to_wallets') and len(value['to_wallets']) > 0:
                            wallet_id = await pool.fetchval(sql.WALLET_ID, value['to_wallets'][0]['id'])
                            to_wallets_id = await pool.fetchval(sql.ADD_TO_WALLETS, value['to_wallets'][0]['before'],
                                                                value['to_wallets'][0]['amount'],
                                                                value['to_wallets'][0]['after'], wallet_id,
                                                                value['date'], value['to_wallets'][0]['currency'])
                        else:
                            to_wallets_id = None

                        await pool.fetchval(sql.ADD_OPERATION, value['id'], type_id, value['date'], value['description'], user_id, from_wallets_id, to_wallets_id, value['group'])
        return "Операции перенесены."
    except Exception as exc:
        return f"При переносе данных произошла ошибка {exc}"
