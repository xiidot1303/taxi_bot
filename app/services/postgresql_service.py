import psycopg2
from config import (
    PG_HOST,
    PG_NAME,
    PG_USER,
    PG_PASSWORD,
    PG_PORT
)

def connect_db():
    con = psycopg2.connect(
        database=PG_NAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    return con

def get_phone_id(phone):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"""SELECT id FROM phone WHERE phonenum='{phone}';""")
    result = cursor.fetchone()
    phone_id = result[0] if result else None
    con.close()
    return phone_id

def get_years_of_order(phone_id):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"""SELECT EXTRACT(YEAR FROM endtime) AS month_index FROM "order" WHERE phone_id = {phone_id} AND status=100;""")
    result = cursor.fetchall()
    years = [int(i[0]) for i in result]
    con.close()
    return years
    

def get_months_of_order(phone_id, year):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"""SELECT EXTRACT(MONTH FROM endtime) AS month_index FROM "order" WHERE EXTRACT(YEAR FROM endtime) = {year} AND phone_id = {phone_id} AND status=100;""")
    result = cursor.fetchall()
    months = [int(i[0]) for i in result]
    con.close()
    return months

def get_days_of_order(phone_id, year, month):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"""SELECT EXTRACT(DAY FROM endtime) AS month_index FROM "order" WHERE EXTRACT(YEAR FROM endtime) = {year} AND EXTRACT(MONTH FROM endtime) = {month} AND phone_id = {phone_id} AND status=100;""")
    result = cursor.fetchall()
    days = [int(i[0]) for i in result]
    con.close()
    return days

def get_orders_by_date(phone_id, year, month, day):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"""SELECT src, dst, starttime, endtime, executor_id, amount, distance, standtime, waittime, street, house, dststreet, dsthouse FROM "order" WHERE EXTRACT(YEAR FROM endtime) = {year} AND EXTRACT(MONTH FROM endtime) = {month} AND EXTRACT(DAY FROM endtime) = {day} AND phone_id = {phone_id} AND status=100;""")
    result = cursor.fetchall()
    con.close()
    return result

# def get_auto_id(executor_id):
#     con = connect_db()
#     cursor = con.cursor()
#     cursor.execute(f"SELECT auto_id FROM executor WHERE id={executor_id}")
#     result = cursor.fetchone()
#     con.close()
#     return result

def get_car_info(auto_id):
    if not auto_id:
        return None
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"SELECT autonum, color, brand, model, lastname, firstname, phone FROM auto WHERE id={auto_id}")
    result = cursor.fetchone()
    con.close()
    return result