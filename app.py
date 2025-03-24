# app.py - Streamlit App for Boycott List Lookup

import streamlit as st
import pandas as pd

# Türkçe karakterleri normalize eden yardımcı fonksiyon
def normalize(text):
    translation_table = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return text.translate(translation_table).lower().strip()

# Load the dataset from the data folder
df = pd.read_csv("data/boycott_list.csv")

st.set_page_config(page_title="Boykot Listesi Sorgulama", layout="centered")

st.title("📛 Boykot Listesi Sorgulama")

st.markdown("""
Bu uygulama, **Türkiye'deki Adalet ve Kalkınma Partisi (AKP) iktidarıyla doğrudan veya dolaylı şekilde bağlantılı olan şirketleri** içeren bir boykot listesini içermektedir.

Listedeki şirketler:
- Hükümete yakın sermaye gruplarına ait,
- Rejim yanlısı medya, eğitim, sağlık, perakende ve gıda sektörlerinde faaliyet gösteren,
- Geçmişte muhalif hareketlere (örneğin Gezi Direnişi) veya **2025 Türkiye'de hükûmet karşıtı protestolarına** karşı tavır almış veya destek vermemiş kuruluşlardır.

Bu araç, bireylerin etik ve politik hassasiyetlerine göre alışveriş tercihlerini yapabilmeleri için hazırlanmıştır.

📌 Aşağıdan bir şirket adını yazarak listede olup olmadığını kontrol edebilirsiniz.
""")

# Açılır liste (dropdown) ile seçim
company_list = sorted(df['Şirket'].dropna().unique())
query = st.selectbox("🏢 Şirket seçin: (Liste uzun olabilir, şirket adını yazarak hızlıca filtreleyebilirsiniz.)", ["-- Şirket seçin --", "🔎 Tüm listeyi göster"] + company_list)

if query == "🔎 Tüm listeyi göster":
    st.info("Tüm boykot listesi aşağıda görüntülenmektedir.")
    st.dataframe(df, use_container_width=True)
elif query and query != "-- Şirket seçin --":
    results = df[df['Şirket'].str.lower() == query.lower()]
    if not results.empty:
        row = results.iloc[0]
        # st.success(f"✅ 1 sonuç bulundu:")
        st.markdown(f"**{row['Şirket']} - {row['Kategori']}**")
        st.markdown(f"{row['Sahibi/Not']}")
    else:
        st.error("❌ Şirket boykot listesinde bulunamadı.")
else:
    st.info("Lütfen aramak için bir şirket seçin.")