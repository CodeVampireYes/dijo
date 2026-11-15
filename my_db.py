import sqlite3

conn = sqlite3.connect('my_db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_money (month_years TEXT,
                                        month_money TEXT,
                                        norma_month TEXT,
                                        real_hours_month TEXT,
                                        plus_day TEXT,
                                        plus_night TEXT,
                                        stavka TEXT,
                                        premia TEXT)
''')

conn.close()

