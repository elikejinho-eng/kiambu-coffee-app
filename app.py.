import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

st.set_page_config(page_title="KIAMBU COFFEE", layout="centered", page_icon="☕")

# HIDE ALL ENGLISH SYSTEM TEXT
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0B3D2E, #1B5E20) !important; }
html, body, p, div, label { font-size: 20px !important; }
[data-testid="InputInstructions"] { display: none !important; }
.stNumberInput input, .stTextInput input { font-size: 24px !important; font-weight: bold !important; height: 60px !important; }
.stButton button { font-size: 22px !important; font-weight: bold !important; height: 65px !important; border-radius: 15px !important; }
.big-card { background: white; border-radius: 18px; padding: 15px; text-align: center; border: 4px solid; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

if 'kitabu' not in st.session_state:
    st.session_state.kitabu = []

if 'price_ripe' not in st.session_state:
    st.session_state.price_ripe = 120
if 'price_dried' not in st.session_state:
    st.session_state.price_dried = 60

# LANGUAGE
lang = st.selectbox("🌐 CHAGUA LUGHA / CHOOSE LANGUAGE", ["Kiswahili", "English", "Gikuyu"])

T = {
 "Kiswahili": {"app":"MASHAMBA YA KAHAWA KIAMBU", "bei":"BEI ZA LEO", "ripe":"Kahawa Mbivu", "dried":"Mbuni Kavu", "jina":"Jina la Mkulima", "shamba":"Shamba", "tarehe":"Tarehe", "jumla":"Jumla ya Leo (mfano 150)", "uliza":"Unaingiza gani?", "weka_ripe":"Weka Mbivu KG", "weka_dried":"Weka Mbuni KG", "hifadhi":"💾 HIFADHI", "data":"Data Yote", "kilo":"KILO", "pesa":"PESA"},
 "English": {"app":"KIAMBU COFFEE FARMS", "bei":"TODAY PRICES", "ripe":"Ripe Berries", "dried":"Dried Berries", "jina":"Farmer Name", "shamba":"Farm", "tarehe":"Date", "jumla":"Total Today (e.g. 150)", "uliza":"What are you entering?", "weka_ripe":"Enter Ripe KG", "weka_dried":"Enter Dried KG", "hifadhi":"💾 SAVE", "data":"All Data", "kilo":"KILOS", "pesa":"MONEY"},
 "Gikuyu": {"app":"MIGUNDA YA KAHAWA KIAMBU", "bei":"MITENGO YA RlU", "ripe":"Kahawa Njeku", "dried":"Mbuni", "jina":"Riitwa", "shamba":"Mugunda", "tarehe":"Muthenya", "jumla":"Magetha ma Umuthi (ta 150)", "uliza":"Ni kii urenda?", "weka_ripe":"Ikira Njeku KG", "weka_dried":"Ikira Mbuni KG", "hifadhi":"💾 BIKA", "data":"Data Ciothe", "kilo":"KIRO", "pesa":"MBECA"},
}[lang]

st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; text-align:center; border:4px solid #FFD700;'><h2 style='margin:0; color:#0B3D2E;'>☕ {T['app']}</h2><p style='margin:5px 0 0 0; color:green; font-weight:bold;'>Kahawa yetu mapato bora</p></div>", unsafe_allow_html=True)
st.write("")

# BEI - EDITABLE
c1,c2 = st.columns(2)
with c1:
    st.session_state.price_ripe = st.number_input(f"🍒 {T['ripe']} / KG", value=st.session_state.price_ripe)
with c2:
    st.session_state.price_dried = st.number_input(f"🟤 {T['dried']} / KG", value=st.session_state.price_dried)

df = pd.DataFrame(st.session_state.kitabu)
if not df.empty:
    ripe_sum = df[df["Aina"]=="Ripe"]["Kilos"].sum() if "Aina" in df.columns else 0
    dried_sum = df[df["Aina"]=="Dried"]["Kilos"].sum() if "Aina" in df.columns else 0
    ripe_pesa = df[df["Aina"]=="Ripe"]["Pesa"].sum() if "Aina" in df.columns else 0
    dried_pesa = df[df["Aina"]=="Dried"]["Pesa"].sum() if "Aina" in df.columns else 0
    total = df["Pesa"].sum()
    st.markdown(f"""
    <div class='big-card' style='border-color:#dc2626;'><b>🍒 {T['ripe']}</b><br><span style='font-size:32px; font-weight:900;'>{ripe_sum} {T['kilo']}</span><br>KSH {ripe_pesa:,.0f}</div>
    <div class='big-card' style='border-color:#5D3311;'><b>🟤 {T['dried']}</b><br><span style='font-size:32px; font-weight:900;'>{dried_sum} {T['kilo']}</span><br>KSH {dried_pesa:,.0f}</div>
    <div class='big-card' style='border-color:#FFD700; background:#FFFDE7;'><b>🏆 TOTAL</b><br><span style='font-size:38px; font-weight:900; color:#0B3D2E;'>KSH {total:,.0f}</span></div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader(f"📖 KITABU - {T['app']}")

jina = st.text_input(T['jina'], value="Kitonyi", placeholder="Weka jina hapa")
shamba_opts = ["Shamba 1","Shamba 2","Shamba 3"] if lang=="Kiswahili" else ["Farm 1","Farm 2","Farm 3"] if lang=="English" else ["Mugunda 1","Mugunda 2","Mugunda 3"]
shamba = st.selectbox(T['shamba'], shamba_opts)
tarehe = st.date_input(T['tarehe'], value=date.today())

total_str = st.text_input(T['jumla'], value="150", placeholder="Weka nambari hapa")
try:
    total_kg = float(total_str)
except:
    total_kg = 0

st.write(f"**{T['uliza']}**")
mode = st.radio("", [f"🍒 {T['ripe']}", f"🟤 {T['dried']}"], horizontal=True)

if "🍒" in mode:
    ripe_str = st.text_input(T['weka_ripe'], value="140", placeholder="Weka nambari hapa")
    try: ripe_kg = float(ripe_str)
    except: ripe_kg = 0
    dried_kg = total_kg - ripe_kg
else:
    dried_str = st.text_input(T['weka_dried'], value="10", placeholder="Weka nambari hapa")
    try: dried_kg = float(dried_str)
    except: dried_kg = 0
    ripe_kg = total_kg - dried_kg

if dried_kg <0: dried_kg=0
if ripe_kg <0: ripe_kg=0

pesa_ripe = ripe_kg * st.session_state.price_ripe
pesa_dried = dried_kg * st.session_state.price_dried

st.info(f"🍒 {ripe_kg}kg = KSH {pesa_ripe:,.0f} | 🟤 {dried_kg}kg = KSH {pesa_dried:,.0f} | **TOTAL KSH {pesa_ripe+pesa_dried:,.0f}**")

if st.button(T['hifadhi'], use_container_width=True, type="primary"):
    if total_kg <=0:
        st.error("Weka kilo!")
    else:
        if ripe_kg>0:
            st.session_state.kitabu.append({"Tarehe":str(tarehe),"Jina":jina,"Shamba":shamba,"Aina":"Ripe","Kilos":ripe_kg,"Bei":st.session_state.price_ripe,"Pesa":pesa_ripe})
        if dried_kg>0:
            st.session_state.kitabu.append({"Tarehe":str(tarehe),"Jina":jina,"Shamba":shamba,"Aina":"Dried","Kilos":dried_kg,"Bei":st.session_state.price_dried,"Pesa":pesa_dried})
        st.success("Imehifadhiwa! / Saved!")
        st.balloons()
        st.rerun()

if st.session_state.kitabu:
    st.divider()
    st.subheader(T['data'])
    df_show = pd.DataFrame(st.session_state.kitabu)
    st.dataframe(df_show, use_container_width=True)
    st.download_button("📥 Pakua CSV", df_show.to_csv(index=False).encode('utf-8'), "kiambu_coffee.csv", "text/csv", use_container_width=True)
    
    if len(df_show)>1:
        fig = px.bar(df_show, x="Tarehe", y="Kilos", color="Aina", barmode="group", color_discrete_map={"Ripe":"#dc2626","Dried":"#5D3311"})
        st.plotly_chart(fig, use_container_width=True)
