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

conn = sqlite3.connect('my_db_dijo.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_recept (id_p TEXT,
                                        indeks TEXT,
                                        szt TEXT,
                                        klient TEXT,
                                        rec TEXT,
                                        waga_kesa TEXT,
                                        rozmiar TEXT,
                                        masa_placka TEXT,
                                        masa_opak TEXT,
                                        wilgot TEXT,
                                        aw TEXT,
                                        owal TEXT,
                                        vs TEXT,
                                        wypiek TEXT)
''')

conn.close()

