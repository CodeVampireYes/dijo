import sqlite3
import pandas as pd
import streamlit as st

st.subheader("🔍 Поиск записи по ID в базе данных")

# Поле для ввода ID, который нужно найти
search_id = st.text_input("Введите ID для поиска", key="search_id_input")

if st.button("Найти запись"):
    if len(search_id) > 0:
        conn = sqlite3.connect("my_db_dijo.db")

        # Используем pandas, чтобы сразу подтянуть и данные, и названия колонок
        query = "SELECT * FROM my_recept WHERE id_p = ?"
        df_result = pd.read_sql(query, conn, params=(search_id,))

        conn.close()

        if not df_result.empty:
            st.success(f"Запись с ID `{search_id}` успешно найдена!")

            # Выводим таблицу с результатами (Streamlit автоматически покажет названия колонок)
            st.dataframe(df_result, hide_index=True)

            # Альтернативный вариант (вертикальный список "Колонка: Значение"):
            # st.write("### Детали записи:")
            # for col in df_result.columns:
            #     st.text(f"{col}: {df_result.iloc[0][col]}")
        else:
            st.warning(f"Запись с ID `{search_id}` не найдена в базе данных.")
    else:
        st.warning("Пожалуйста, введите ID для поиска.")