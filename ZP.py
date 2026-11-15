import sqlite3
import pandas as pd
import streamlit as st
from add_db import input_bar
import my_db

# 1. Первичная настройка страницы (обязательно первой командой Streamlit)
st.set_page_config(page_title="Dijo", page_icon="🌯", layout="wide")


# ==========================================
# ДОБАВЛЕННАЯ АВТОРИЗАЦИЯ ПО ПАРОЛЮ
# ==========================================
def check_password():
  """Возвращает True, если пользователь ввел правильный пароль."""
  if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

  if st.session_state.password_correct:
    return True

  # Безопасно получаем пароль: если файла секретов нет (локально), используется "1234"
  try:
    correct_password = st.secrets["APP_PASSWORD"]
  except Exception:
    correct_password = "1234"

  password = st.text_input("🔒 Введите пароль для доступа к приложению:", type="password")

  if password == correct_password:
    st.session_state.password_correct = True
    st.rerun()
  elif password:
    st.error("😕 Неверный пароль")

  return False


# Если пароль не введен — останавливаем выполнение приложения
if not check_password():
    st.stop()


# ==========================================


def load_data_from_db():
    conn = sqlite3.connect("my_db.db")
    df = pd.read_sql(
        "SELECT month_years as data, month_money as Зп FROM my_money", conn
    )
    conn.close()

    if not df.empty:
        # 1. Превращаем текстовую дату (например, "7.25" или "01.26") в настоящий datetime.
        # format='%m.%y' говорит Pandas, что у нас сначала месяц, потом точка, потом двузначный год.
        df["dt"] = pd.to_datetime(df["data"], format="%m.%y", errors="coerce")

        # 2. Сортируем строго по реальному времени от старых к новым
        df = df.sort_values(by="dt", ascending=True)

        # 3. Возвращаем исходный текстовый вид колонки 'data' (чтобы в таблице и на графике красиво отображалось),
        # но порядок строк теперь идеальный!
        df = df.drop(columns=["dt"]).reset_index(drop=True)

    return df


# Вызываем форму ввода (добавления данных)
input_bar()

# Загружаем актуальные данные из базы данных
df = load_data_from_db()

st.divider()
#########################

# Проверяем, есть ли вообще записи в базе
if df.empty:
    st.warning("В базе данных пока нет записей.")
else:
    # Выводим таблицу (оставляем текст как есть)
    st.dataframe(df, height="content", hide_index=True)

    # Для графика делаем копию, переводим 'Зп' в числа и ставим дату индексом
    # Для графика делаем копию и переводим 'Зп' в числа
    df_chart = df.copy()
    df_chart["Зп"] = pd.to_numeric(df_chart["Зп"], errors="coerce")

    # Переводим колонку 'data' в настоящий datetime прямо в df_chart для правильной оси X
    df_chart["data_dt"] = pd.to_datetime(
        df_chart["data"], format="%m.%y", errors="coerce"
    )

    st.divider()

    # Строим график, явно указав x='data_dt' (но можно подписать или оставить как есть)
    # Streamlit отлично понимает datetime и выстроит их строго по временной шкале слева направо!
    st.line_chart(df_chart, x="data_dt", y="Зп")

    st.divider()
    ###############################

    # 1. Создаем 3 колонки
    col1, col2, col3 = st.columns(3, vertical_alignment="top")

    # Превращаем колонку 'Зп' в числа только для расчетов AVG
    zp_numeric = pd.to_numeric(df["Зп"], errors="coerce")
    row_count = len(df)

    # 2. Выводим данные с проверкой количества строк
    if row_count >= 3:
        col1.write(f"AVG-3: {int(zp_numeric.iloc[-3:].mean())}")
    else:
        col1.write("AVG-3: нужно >= 3")

    if row_count >= 6:
        col2.write(f"AVG-6: {int(zp_numeric.iloc[-6:].mean())}")
    else:
        col2.write("AVG-6: нужно >= 6")

    if row_count >= 12:
        col3.write(f"AVG-12: {int(zp_numeric.iloc[-12:].mean())}")
    else:
        col3.write("AVG-12: нужно >= 12")

st.divider()
###############################

col6, col7 = st.columns(2)
col8, col9 = st.columns(2)

norma_hours = col6.number_input("Норма", value=180)
fact_hours = col7.number_input("Фактически часов", value=180)

over_day = col8.number_input('День', value=0)
over_night = col9.number_input('Ночь', value=0)

my_zp = 7000
my_premia = 600

# math#

col10, col11 = st.columns(2)

in_hours = my_zp / norma_hours
in_hours_50 = in_hours / 2
in_hours_100 = in_hours * 2
surplus = (fact_hours - norma_hours) * in_hours * 1.75

brutto = my_zp + my_premia + surplus + (over_day * in_hours_50 * 12) + (over_night * in_hours_100 * 12)
netto = brutto * 0.69

col10.write(f"**Brutto:** {brutto:.2f}")
col11.write(f"### Netto: {netto:.2f}")