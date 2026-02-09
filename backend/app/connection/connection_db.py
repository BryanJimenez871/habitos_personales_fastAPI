import os
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

class ConnectionDB:
    _DATABASE = os.getenv("POSTGRES_DB")
    _USERNAME = os.getenv("POSTGRES_USER")
    _PASSWORD = os.getenv("POSTGRES_PASSWORD")
    _DB_PORT = '5432'
    _HOST = os.getenv("POSTGRES_HOST")
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
                # sys.exit()# si hago esto muere  el programa entero, el servidor, la base de datos.
                raise RuntimeError("Error creando el pool de conexiones") from e
        return cls._pool

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()