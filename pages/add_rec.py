import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Аналитика", page_icon="📊", layout="wide"
)

id_p = st.text_input('id')
indeks = st.text_input('indeks')
szt = st.text_input('szt')
klient = st.text_input('klient')
rec = st.text_input('rec')
waga_kesa = st.text_input('waga_kesa')
rozmiar = st.text_input('rozmiar')
masa_placka = st.text_input('masa_placka')
masa_opak = st.text_input('masa_opak')
wilgot = st.text_input('wilgot')
aw = st.text_input('aw')
owal = st.text_input('owal')
vs = st.text_input('vs', value='1.9')
wypiek = st.text_input('wypiek')

if st.button('Добавить'):
    if len(id_p) > 0 and len(indeks) > 0 and len(szt) > 0 and len(klient) > 0 and len(rec) > 0 and len(waga_kesa) > 0 and len(rozmiar) > 0 and len(masa_placka) > 0 and len(masa_opak) > 0 and len(wilgot) > 0 and len(aw) > 0 and len(owal) > 0 and len(vs) > 0 and len(wypiek) > 0:
        conn = sqlite3.connect("my_db_dijo.db")
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO my_recept VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
        id_p, indeks, szt, klient, rec, waga_kesa, rozmiar, masa_placka, masa_opak, wilgot, aw, owal, vs, wypiek))
        conn.commit()
        conn.close()

        st.write('Добавлено в бд')
    else:
        st.write('нет данных')



