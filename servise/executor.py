import json
from datetime import datetime
import os

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
        filename = os.path.dirname(os.path.realpath(__file__))+'\wallets.json'
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            async with JobDb() as pool:
                for key in data:
                    if key['show'] is None:
                        show = 'visible'
                    else:
                        show = key['show']
                    if key['verified'] is None:
                        date = None
                    else:
                        if len(key['verified']) == 20:
                            date = datetime.strptime(key['verified'][:-1], '%Y-%m-%dT%H:%M:%S')
                        elif len(key['verified']) == 27:
                            date = datetime.strptime(key['verified'][:-8], '%Y-%m-%dT%H:%M:%S')

                    user_id = await pool.fetchval(sql.USER_ID_NEW, key['holder'])
                    await pool.fetchrow(sql.NEW_WALLET, key['id'], user_id, key['name'], key['amount'],
                                        key['currency'], key['active'], key['pinned'], key['pin_on_main'],
                                        date, key['description'], key['status'], show,
                                        key['color'])
        return "Кошельки успешно перенесены"
    except Exception as exc:
        return f"При переносе данных произошла ошибка {exc}"


async def create_operation():
    # try:
        filename = os.path.dirname(os.path.realpath(__file__))+'\operations.json'
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for value in data:
                if value['date'] is None:
                    date = None
                else:
                    if len(value['date']) == 20:
                        date = datetime.strptime(value['date'][:-1], '%Y-%m-%dT%H:%M:%S')
                    elif len(value['date']) == 27:
                        date = datetime.strptime(value['date'][:-8], '%Y-%m-%dT%H:%M:%S')
                    date_start = datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                    if date > date_start:
                        async with JobDb() as pool:

                            if value['type'] in ['Добавление кошелька', 'Удаление кошелька']:
                                continue
                            elif value['type'] == "write_balance":
                                type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                                user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                                wallet_id = await pool.fetchval(sql.WALLET_ID, value['wallet_id'])
                                write_id = await pool.fetchval(sql.ADD_WRITE_BALANSE, date, wallet_id, value['amount'], value['currency'], user_id)
                                await pool.fetchval(sql.ADD_OPERATION_WRITE, value['id'], type_id, date, user_id, write_id)

                            elif value['type'] == "Корректировка":
                                type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                                user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                                if value.get('old') and len(value['old']) > 0:
                                    if value['old']['name'] == "wal1":
                                        continue
                                    else:
                                        wallet_id = await pool.fetchval(sql.WALLET_ID, value['old']['id'])
                                        date_new = datetime.now()
                                        old_id = await pool.fetchval(sql.ADD_OLD, wallet_id, value['old']['amount'], date, value['old']['description'], value['old']['status'], value['old']['color'], date_new, value['old']['name'], value['old']['currency'])
                                else:
                                    old_id = None

                                if value.get('new') and len(value['new']) > 0:
                                    if value['new']['name'] == "wal1":
                                        continue
                                    else:
                                        wallet_id = await pool.fetchval(sql.WALLET_ID, value['new']['id'])
                                        date_new = datetime.now()
                                        new_id = await pool.fetchval(sql.ADD_NEW, wallet_id, value['new']['amount'], date, value['new']['description'], value['new']['status'], value['new']['color'], date_new, value['new']['name'], value['new']['currency'])
                                else:
                                    new_id = None

                                if value.get('from_wallets') and len(value['from_wallets']) > 0:
                                    wallet_id = await pool.fetchval(sql.WALLET_ID, value['from_wallets'][0]['id'])
                                    from_wallets = await pool.fetchval(sql.ADD_FROM_WALLETS,
                                                                          value['from_wallets'][0]['before'],
                                                                          value['from_wallets'][0]['amount'],
                                                                          value['from_wallets'][0]['after'], wallet_id,
                                                                          date, value['from_wallets'][0]['currency'])
                                    from_wallets_id = str(from_wallets)
                                else:
                                    from_wallets_id = None

                                if value.get('to_wallets') and len(value['to_wallets']) > 0:
                                    wallet_id = await pool.fetchval(sql.WALLET_ID, value['to_wallets'][0]['id'])
                                    to_wallets = await pool.fetchval(sql.ADD_TO_WALLETS, value['to_wallets'][0]['before'],
                                                                            value['to_wallets'][0]['amount'],
                                                                            value['to_wallets'][0]['after'], wallet_id,
                                                                            date, value['to_wallets'][0]['currency'])
                                    to_wallets_id = str(to_wallets)
                                else:
                                    to_wallets_id = None

                                await pool.fetchval(sql.ADD_OPERATION_KOR, value['id'], type_id, date, value['description'], user_id, old_id, new_id, value['group'], from_wallets_id, to_wallets_id)

                    # else:
                    #     type_id = await pool.fetchval(sql.TYPE_ID, value['type'])
                    #     user_id = await pool.fetchval(sql.USER_ID, value['user']['id'])
                    #     if value.get('from_wallets') and len(value['from_wallets']) > 0:
                    #         wallet_id = await pool.fetchval(sql.WALLET_ID, value['from_wallets'][0]['id'])
                    #         from_wallets_id = await pool.fetchval(sql.ADD_FROM_WALLETS,
                    #                                               value['from_wallets'][0]['before'],
                    #                                               value['from_wallets'][0]['amount'],
                    #                                               value['from_wallets'][0]['after'], wallet_id,
                    #                                               value['date'], value['from_wallets'][0]['currency'])
                    #     else:
                    #         from_wallets_id = None
                    #     if value.get('to_wallets') and len(value['to_wallets']) > 0:
                    #         wallet_id = await pool.fetchval(sql.WALLET_ID, value['to_wallets'][0]['id'])
                    #         to_wallets_id = await pool.fetchval(sql.ADD_TO_WALLETS, value['to_wallets'][0]['before'],
                    #                                             value['to_wallets'][0]['amount'],
                    #                                             value['to_wallets'][0]['after'], wallet_id,
                    #                                             value['date'], value['to_wallets'][0]['currency'])
                    #     else:
                    #         to_wallets_id = None
                    #
                    #     await pool.fetchval(sql.ADD_OPERATION, value['id'], type_id, value['date'], value['description'], user_id, from_wallets_id, to_wallets_id, value['group'])
        return "Операции перенесены."
    # except Exception as exc:
    #     return f"При переносе данных произошла ошибка {exc}"
