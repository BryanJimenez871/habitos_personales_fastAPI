from app.connection.connection_db import ConnectionDB
from app import schema


class DailyHabitsCrud:
    @classmethod
    async def insert_daily(cls, daily_habit: schema.DailyHabitsCreateSchema):
        sql = """
              INSERT INTO registro_habitos (id_habito,id_fecha, completado) 
              VALUES (%s, %s, %s) RETURNING id_registro;
              """
        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(sql, (daily_habit.habit.habit_id, daily_habit.date.date_id, daily_habit.complet))
                generated_id = (await cursor.fetchone())[0]
                return generated_id

    @classmethod
    async def select_join(cls):
        sql = '''
        SELECT 
            r.id_registro, 
            h.id_habito,
            h.nombre_habito,
            h.tipo_habito,
            f.id_fecha,
            f.fecha_habitos, 
            r.completado 
        FROM registro_habitos r 
        JOIN habitos h ON r.id_habito = h.id_habito 
        JOIN fecha f ON r.id_fecha = f.id_fecha 
        ORDER BY f.fecha_habitos;
    '''
        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                records_join = await cursor.fetchall()
                list_records_join = []
                for record in records_join:
                    habit = schema.HabitSchema(habit_id=record[1], habit_name=record[2], habit_type=record[3])
                    date = schema.DateSchema(date_id=record[4], habit_date=record[5])
                    daily_habit = schema.DailyHabitsSchema(
                        daily_id=record[0],
                        complet=record[6],
                        habit=habit,
                        date=date
                    )
                    list_records_join.append(daily_habit)
        return list_records_join

    @classmethod
    async def select_pie_chart(cls):
        sql = '''
        SELECT  
            h.tipo_habito,
            r.completado
        FROM registro_habitos r 
        JOIN habitos h ON r.id_habito = h.id_habito;
        '''

        pool = await ConnectionDB.get_pool()

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                records_pie = await cursor.fetchall()
                list_records_pie = []
                for record in records_pie:
                    habit = schema.HabitSchema(habit_type=record[0])
                    daily_habit = schema.DailyHabitsSchema(
                        complet=record[1],
                        habit=habit
                    )
                    list_records_pie.append(daily_habit)
        return list_records_pie

    @classmethod
    async def delete_habit(cls, habit_id):
        sql = 'DELETE FROM habitos WHERE id_habito = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (habit_id,))
                return cursor.rowcount

    @classmethod
    async def delete_id_habit(cls, habit_id):
        sql = 'DELETE FROM registro_habitos WHERE id_habito = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (habit_id,))
                return cursor.rowcount

    @classmethod
    async def delete_id_daily(cls, daily_id):
        sql = 'DELETE FROM registro_habitos WHERE id_registro = %s;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (daily_id,))
                return cursor.rowcount

    @classmethod
    async def delete_all(cls):
        sql = 'DELETE FROM registro_habitos;'
        pool = await ConnectionDB.get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                return cursor.rowcount