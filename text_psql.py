import psycopg2
con = psycopg2.connect(
    database="taxi",
    user="dilmurod",
    password="ZwLCOWSIJKdWmMBixhU",
    host="213.230.124.224",
    port=5432
)

cursor = con.cursor()

cursor.execute("""SELECT waittime FROM "order" WHERE waittime IS NOT NULL LIMIT 10;""")
result = cursor.fetchall()
print(result)
con.close()