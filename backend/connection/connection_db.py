import sys

from psycopg_pool import AsyncConnectionPool


class ConnectionDB:
    _DATABASE = 'habitos_personales'
    _USERNAME = '******'
    _PASSWORD = '******'
    _DB_PORT = '5432'
    _HOST = '127.0.0.1'
    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            try:
                params = {
                    "dbname": cls._DATABASE,
                    "user": cls._USERNAME,
                    "password": cls._PASSWORD,
                    "host": cls._HOST,
                    "port": cls._DB_PORT
                }

                cls._pool = AsyncConnectionPool(conninfo="", kwargs=params,
                                           min_size=cls._MIN_CON,
                                           max_size=cls._MAX_CON,
                                           open =False)
                await cls._pool.open()
                return cls._pool
            except Exception as e:
                print(e)
                sys.exit()
        return cls._pool

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()