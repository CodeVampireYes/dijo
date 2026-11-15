import sqlite3
import streamlit as st


# Функция для сохранения (сама открывает и закрывает соединение)
def add_db_data_zp(month_years, month_money):
  conn = sqlite3.connect('my_db.db')
  cursor = conn.cursor()

  cursor.execute(
      """
        INSERT INTO my_money (
            month_years,
            month_money  
        ) 
        VALUES (?, ?)
    """,
      (month_years, month_money),
  )

  conn.commit()
  conn.close()


def input_bar()
  # Поля ввода
  input_data = st.text_input('Data')
  input_zp = st.text_input('Zp')

  st.write(f'Длина введенного месяца: {len(input_data)}')

  # Кнопка сохранения (работает через обычный if, что намного проще для форм)
  if st.button('Добавить в бд'):
    if len(input_data) > 0 and len(input_zp) > 0:
      add_db_data_zp(input_data, input_zp)
      st.success('Успешно добавлено в базу!')
    else:
      st.warning('Заполни оба поля перед отправкой!')