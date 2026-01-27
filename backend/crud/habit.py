from backend.connection.connection_db import ConnectionDB
from backend import schema


class HabitCrud:
    @classmethod
    async def insert_habit(cls, habit: schema.HabitCreateSchema):
        sql = """
        INSERT INTO habitos(nombre_habito, tipo_habito, descripcion) 
        VALUES (%s, %s, %s) RETURNING id_habito;
        """
        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (habit.habit_name, habit.habit_type, habit.description))
                generated_id = (await cursor.fetchone())[0]
                #habit.habit_id = generated_id # esto se hacía antes porque la BD se conectaba directamente con el backend, pero ahora es PYTHON(PYSIDE6) -> API -> BD
                # Ahora es la API que hace que el id generado se congenie con el backend
                return generated_id

    @classmethod
    async def select(cls):
        sql = 'SELECT * FROM habitos ORDER BY id_habito;'
        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                records = await cursor.fetchall()
                list_habits = []
                for record in records:
                    habit = schema.HabitSchema(
                        habit_id=record[0],
                        habit_name=record[1],
                        habit_type=record[2],
                        description=record[3]
                    )
                    list_habits.append(habit)
                return list_habits

    @classmethod
    async def search_name(cls,name_habit: str):
        sql = 'SELECT id_habito FROM habitos WHERE nombre_habito = %s;'
        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (name_habit,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
            return None

    @classmethod
    async def delete_habit(cls, habit_id):
        sql = 'DELETE FROM habitos WHERE id_habito = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (habit_id,))
                return cursor.rowcount

    @classmethod
    async def delete_all(cls):
        sql = 'DELETE FROM habitos;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                return cursor.rowcount