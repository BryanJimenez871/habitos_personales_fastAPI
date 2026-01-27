from backend.connection.connection_db import ConnectionDB
from backend.schema import HabitSchema, DailyHabitsSchema
from backend.schema.date import DateSchema, DateCreateSchema

class DateCrud:

    @classmethod
    async def insert_date(cls, date:DateCreateSchema):
        sql = 'INSERT INTO fecha(fecha_habitos) VALUES (%s) RETURNING id_fecha;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (date.habit_date,))
                generated_id = (await cursor.fetchone())[0]
            return generated_id

    @classmethod
    async def select_range_date(cls, start_date, end_date):
        sql = '''
        SELECT 
            h.tipo_habito,
            r.completado,
            f.fecha_habitos
        FROM registro_habitos r 
        JOIN habitos h ON r.id_habito = h.id_habito 
        JOIN fecha f ON r.id_fecha = f.id_fecha 
        WHERE fecha_habitos >= %s
        AND fecha_habitos <  %s;
        '''
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (start_date, end_date))
                records_cake = await cursor.fetchall()
                list_habits_cake = []
                for record in records_cake:
                    habit = HabitSchema(habit_type=record[0])
                    date = DateSchema(habit_date=record[2])
                    habit_record = DailyHabitsSchema(
                        complet=record[1],
                        habit = habit,
                        date = date
                    )
                    list_habits_cake.append(habit_record)
        return list_habits_cake

    @classmethod
    async def select_only_day(cls, date):
        sql = '''
        SELECT 
            h.tipo_habito,
            r.completado,
            f.fecha_habitos
        FROM registro_habitos r 
        JOIN habitos h ON r.id_habito = h.id_habito 
        JOIN fecha f ON r.id_fecha = f.id_fecha 
        WHERE fecha_habitos = %s
        '''
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (date,))
                records_cake = await cursor.fetchall()
                list_habits_cake = []
                for record in records_cake:
                    habit = HabitSchema(habit_type=record[0])
                    date = DateSchema(habit_date=record[2])
                    habit_record = DailyHabitsSchema(
                        complet=record[1],
                        habit=habit,
                        date=date
                    )
                    list_habits_cake.append(habit_record)
        return list_habits_cake

    @classmethod
    async def search_date(cls, habit_date):
        sql = 'SELECT id_fecha FROM fecha WHERE fecha_habitos = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (habit_date,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
        return None

    @classmethod
    async def delete_date_id(cls, date_id):
        sql = 'DELETE FROM fecha WHERE id_fecha = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (date_id,))
                return cursor.rowcount

    @classmethod
    async def delete_all(cls):
        sql = 'DELETE FROM fecha;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                return cursor.rowcount