import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px
import requests
st.set_page_config(page_title="KIAMBU COFFEE FARMS", page_icon="kcf_logo.png", layout="wide")
st.sidebar.image("kcf_logo.png", use_container_width=True)
with open("kcf_logo.png", "rb") as f:
    st.sidebar.download_button("👆 Click Logo to Save KCF Logo", f, file_name="KCF_Logo.png", mime="image/png")
# ===== SESSION STATE - CORRECTED =====
if 'users' not in st.session_state:
    st.session_state.users = {"Kitonyi": {"password": "Kejinho@100%", "farm": "1", "phone": "0706144440"}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'lang' not in st.session_state:
    st.session_state.lang = "Gikuyu"
if 'kitabu' not in st.session_state:
    st.session_state.kitabu = [
        {"Tarehe": "2025-10-20", "Jina": "Kitonyi", "Aina": "Ripe Berries", "Shamba": "Mugunda 1", "Kilos": 450,
         "Bei": 120, "Pesa": 54000},
        {"Tarehe": "2025-10-21", "Jina": "Kitonyi", "Aina": "Dried Berries", "Shamba": "Mugunda 1", "Kilos": 45,
         "Bei": 60, "Pesa": 2700},
        {"Tarehe": "2025-10-22", "Jina": "Wanjiku", "Aina": "Ripe Berries", "Shamba": "Mugunda 2", "Kilos": 320,
         "Bei": 120, "Pesa": 38400},
    ]


def get_day_name_translated(d, lang):
    if lang == "Kiswahili":
        days = {"Mon": "Jumatatu", "Tue": "Jumanne", "Wed": "Jumatano", "Thu": "Alhamisi", "Fri": "Ijumaa",
                "Sat": "Jumamosi", "Sun": "Jumapili"}
        months = {"Jan": "Jan", "Feb": "Feb", "Mar": "Mac", "Apr": "Apr", "May": "Mei", "Jun": "Jun", "Jul": "Jul",
                  "Aug": "Ago", "Sep": "Sep", "Oct": "Okt", "Nov": "Nov", "Dec": "Des"}
        return f"{days[d.strftime('%a')]} {d.day} {months[d.strftime('%b')]}"
    elif lang == "Gikuyu":
        days = {"Mon": "Njumatatu", "Tue": "Njumanne", "Wed": "Njumatano", "Thu": "Alahamisi", "Fri": "Ijumaa",
                "Sat": "Jumamosi", "Sun": "Kiumia"}
        return f"{days[d.strftime('%a')]} {d.day} {d.strftime('%b')}"
    else:
        return d.strftime("%a %d %b")


def translate_farm_name(farm_raw, lang):
    raw = str(farm_raw)
    if "3" in raw:
        num = "3"
    elif "2" in raw:
        num = "2"
    else:
        num = "1"
    if lang == "Kiswahili":
        return f"🌿 Shamba {num}"
    elif lang == "Gikuyu":
        return f"🌿 Mugunda {num}"
    else:
        return f"🌿 Farm {num}"


@st.cache_data(ttl=3600)
def get_kiambu_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-1.1714&longitude=36.8356&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,precipitation_probability_max&timezone=Africa/Nairobi&forecast_days=7"
        return requests.get(url, timeout=10).json()
    except:
        return None


def get_farm_advice(precip, temp_max, lang):
    if lang == "English":
        if precip > 15:
            return "🌧️ HEAVY RAIN: Don't prune! Good for FERTILIZER - rain will wash to roots. No harvest."
        elif precip > 5:
            return "🌦️ LIGHT RAIN: Good for FERTILIZER. Wait dry to prune. Harvest morning only."
        elif precip < 2 and temp_max > 24:
            return "☀️ DRY & HOT: BEST for PRUNING & HARVEST! Trees dry, no disease. Prune now!"
        else:
            return "⛅ DRY: Good for PRUNING, HARVEST & SPRAYING. Best farm work time!"
    elif lang == "Kiswahili":
        if precip > 15:
            return "🌧️ MVUA KUBWA: Usikate! Muda mzuri wa MBOLEA - mvua itapeleka mizizini. Usivune."
        elif precip > 5:
            return "🌦️ MVUA KIDOGO: Nzuri kwa MBOLEA. Subiri kuka kukata. Vuna asubuhi tu."
        elif precip < 2 and temp_max > 24:
            return "☀️ KUKAUKA & JOTO: BORA KWA KUKATA & KUVUNA! Miti mikavu, hakuna ugonjwa. Kata sasa!"
        else:
            return "⛅ KUKAUKA: Nzuri kwa KUKATA, KUVUNA & KUNYUNYIZIA. Muda bora wa kazi ya shamba!"
    else:
        if precip > 15:
            return "🌧️ MBUA NYINGI: Ndugakate! Mahinda mega ma THUMU - mbua niikuhithia miri. Ndugathie magetha."
        elif precip > 5:
            return "🌦️ MBUA NINI: Mega ma THUMU. Eterera kuuma kuguata. No uhote kutha rucini tu."
        elif precip < 2 and temp_max > 24:
            return "☀️ KUUMA & URIU: KIGO KWA GUTHINJA & KUTHA! Miti miume, guti muoroto. Thinja riu!"
        else:
            return "⛅ KUUMA: Mega ma GUTHINJA, KUTHA & GUTHEKERERA. Mahinda mega ma wira wa mugunda!"


def moon_phase_on_date(d):
    known_new_moon = datetime(2024, 1, 11)
    diff = (d - known_new_moon).days
    phase = (diff % 29.53) / 29.53
    return phase


def moon_icon_and_name(phase, lang):
    if phase < 0.03 or phase > 0.97:
        icon = "🌑";
        name = "New Moon" if lang == "English" else "Mwezi Mpia" if lang == "Kiswahili" else "Mweri Meru"
        advice = "Plant seedlings, root fertilizer" if lang == "English" else "Panda miche, mbolea ya mizizi" if lang == "Kiswahili" else "Handa mbeu, thumu ya miri"
        coffee = "🌱 PLANTING" if lang == "English" else "🌱 KUPANDA" if lang == "Kiswahili" else "🌱 KUHANDA"
    elif phase < 0.22:
        icon = "🌒";
        name = "Waxing Crescent" if lang == "English" else "Mwezi Unakua" if lang == "Kiswahili" else "Mweri Urakuura"
        advice = "Leaves grow, foliar spray" if lang == "English" else "Majani yanakua, dawa ya majani" if lang == "Kiswahili" else "Mathangu makuura, guthaambia mathangu"
        coffee = "🍃 FOLIAR SPRAY" if lang == "English" else "🍃 DAWA YA MAJANI" if lang == "Kiswahili" else "🍃 GUTHAAMBIA"
    elif phase < 0.28:
        icon = "🌓";
        name = "First Quarter" if lang == "English" else "Robo ya Kwanza" if lang == "Kiswahili" else "Nuthu ya Mbere"
        advice = "Strong growth, good for planting" if lang == "English" else "Ukuaji nguvu, nzuri kupanda" if lang == "Kiswahili" else "Kukura na hinya, mega kuhanda"
        coffee = "🌿 GROWTH" if lang == "English" else "🌿 UKUAJI" if lang == "Kiswahili" else "🌿 KUKURA"
    elif phase < 0.47:
        icon = "🌔";
        name = "Waxing Gibbous" if lang == "English" else "Karibu Mwezi Mkuu" if lang == "Kiswahili" else "Kuhika Mweri Munene"
        advice = "Prepare for harvest" if lang == "English" else "Jitayarishe kuvuna" if lang == "Kiswahili" else "Haririka gutha"
        coffee = "⏳ PREPARE HARVEST" if lang == "English" else "⏳ TAYARI KUVUNA" if lang == "Kiswahili" else "⏳ HARIRIKA KUTHA"
    elif phase < 0.53:
        icon = "🌕";
        name = "Full Moon" if lang == "English" else "Mwezi Mkuu" if lang == "Kiswahili" else "Mweri Munene"
        advice = "BEST HARVEST - berries juicy!" if lang == "English" else "MAVUNO BORA - kahawa tamu!" if lang == "Kiswahili" else "KUTHA KWEGA - kahawa irimu!"
        coffee = "🍒 HARVEST NOW!" if lang == "English" else "🍒 VUNA SASA!" if lang == "Kiswahili" else "🍒 THA RIU!"
    elif phase < 0.72:
        icon = "🌖";
        name = "Waning Gibbous" if lang == "English" else "Mwezi Unapungua" if lang == "Kiswahili" else "Mweri Ukuhinyiha"
        advice = "Harvest, process coffee" if lang == "English" else "Vuna, chakata kahawa" if lang == "Kiswahili" else "Tha, thondeka kahawa"
        coffee = "📦 PROCESS" if lang == "English" else "📦 CHAKATA" if lang == "Kiswahili" else "📦 THONDEKA"
    elif phase < 0.78:
        icon = "🌗";
        name = "Last Quarter" if lang == "English" else "Robo ya Mwisho" if lang == "Kiswahili" else "Nuthu ya Muico"
        advice = "BEST FOR PRUNING!" if lang == "English" else "BORA KWA KUKATA!" if lang == "Kiswahili" else "KIGO KWA GUTHINJA!"
        coffee = "✂️ PRUNE NOW!" if lang == "English" else "✂️ KATA SASA!" if lang == "Kiswahili" else "✂️ THINJA RIU!"
    else:
        icon = "🌘";
        name = "Waning Crescent" if lang == "English" else "Mwezi Unaisha" if lang == "Kiswahili" else "Mweri Uthiraga"
        advice = "Weeding, pest control, prune" if lang == "English" else "Palilia, wadudu, kata" if lang == "Kiswahili" else "Rimira, thukia, thinja"
        coffee = "🌾 WEED & PRUNE" if lang == "English" else "🌾 PALILIA & KATA" if lang == "Kiswahili" else "🌾 RIMIRA & THINJA"
    return icon, name, advice, coffee


st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0B3D2E, #1B5E20, #2E7D32) !important; background-attachment: fixed !important; }
html, body, p, div, label, span { font-size: 22px !important; }
.white-title { color: white !important; font-weight: 900 !important; font-size: 26px !important; text-shadow: 3px 3px 6px black !important; background: rgba(0,0,0,0.4) !important; padding: 12px 15px !important; border-radius: 10px !important; border-left: 6px solid #dc2626 !important; margin: 18px 0 8px 0 !important; }
[data-testid="stWidgetLabel"] { display: none !important; }
div[data-testid="stRadio"] { background: rgba(0,0,0,0.4) !important; padding: 20px !important; border-radius: 15px !important; border: 3px solid white !important; }
div[data-testid="stRadio"] * { color: white !important; }
div[data-testid="stRadio"] label p { color: white !important; font-weight: 900 !important; font-size: 26px !important; text-shadow: 3px 3px 6px black !important; }
.stTextInput input, .stNumberInput input { background: #dc2626 !important; color: white !important; font-size: 30px !important; font-weight: 900 !important; height: 68px !important; border: 4px solid white !important; border-radius: 12px !important; }
.stTextInput input::placeholder { color: #FFCDD2 !important; }
div[data-baseweb="select"] > div, div[data-baseweb="select"] div { background: #dc2626 !important; color: white !important; border: 4px solid white !important; border-radius: 12px !important; min-height: 65px !important; }
div[data-baseweb="select"] span { color: white !important; font-weight: 900 !important; font-size: 24px !important; }
div[data-testid="stDateInput"], div[data-testid="stDateInput"] > div, div[data-testid="stDateInput"] input { background: #dc2626 !important; color: white !important; border: 4px solid white !important; border-radius: 12px !important; }
div[data-testid="stDateInput"] input { font-size: 28px !important; font-weight: 900 !important; }
[data-testid="stSidebar"] .stNumberInput input { background: white !important; color: #dc2626 !important; border: 4px solid #FFD700 !important; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: white !important; font-weight: bold !important; text-shadow: 2px 2px 4px black !important; }
.stButton button { font-size: 24px !important; font-weight: bold !important; height: 65px !important; border-radius: 15px !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #7f1d1d, #B71C1C, #dc2626) !important; }
h1, h2, h3 { color:white !important; text-shadow:3px 3px 8px black !important; }
.big-card { background: white; border-radius: 20px; padding: 20px 15px; text-align: center; border: 4px solid; box-shadow: 0 8px 16px rgba(0,0,0,0.3); min-height: 130px; display: flex; flex-direction: column; justify-content: center; }
.weather-card { background: white; border-radius: 15px; padding: 15px; text-align: center; border: 3px solid #00C853; box-shadow: 0 4px 8px rgba(0,0,0,0.2); min-height: 160px; }
.moon-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 15px; text-align: center; border: 3px solid #FFD700; color:white; min-height: 220px; }
.weather-advice { background: #E8F5E9; border: 3px solid #00C853; border-radius: 12px; padding: 10px; font-weight: bold; color: #0B3D2E; font-size:13px; margin-top:8px; }
.main-tabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.15) !important; border-radius: 15px !important; border: 4px solid #FFD700 !important; padding:8px !important; }
.main-tabs [data-baseweb="tab-list"] button { color: white !important; font-weight: 900 !important; font-size: 22px !important; }
.main-tabs [data-baseweb="tab-list"] button p { color: white !important; font-size: 22px !important; }
.main-tabs [data-baseweb="tab-list"] button[aria-selected="true"] { background: #FFD700 !important; color: #0B3D2E !important; border-radius: 10px !important; }
.main-tabs [data-baseweb="tab-list"] button[aria-selected="true"] p { color: #0B3D2E !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(0,0,0,0.5) !important; border-radius: 12px !important; border: 3px solid white !important; padding:5px !important; }
.stTabs [data-baseweb="tab-list"] button { color: white !important; font-weight: 900 !important; font-size: 18px !important; }
.stTabs [data-baseweb="tab-list"] button p { color: white !important; font-weight: 900 !important; }
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { background: #dc2626 !important; color: white !important; border-radius: 8px !important; }
[data-testid="InputInstructions"] { display: none !important; }
.block-container { max-width: 98% !important; }
</style>
""", unsafe_allow_html=True)

LANG = {
    "English": {"app_title": "KIAMBU COFFEE FARMS", "slogan": "Our coffee better income", "login_title": "Login",
                "name": "Your Name", "password": "Password", "enter": "ENTER", "profile_title": "FARMERS PROFILE",
                "my_profile": "My Profile", "farmer_label": "Kiambu Coffee Farmer", "logout": "Logout",
                "current_prices": "CURRENT PRICES", "ripe_kg_label": "Ripe Berries / KG",
                "dried_kg_label": "Dried Berries / KG", "ripe_display": "Ripe Berries",
                "dried_display": "Dried Berries", "ripe_plain": "Ripe Berries", "dried_plain": "Dried Berries",
                "total_boxes_title": "All Totals", "kilos": "KILOS", "pesa": "MONEY", "total": "TOTAL INCOME",
                "jumla_kg": "kg total", "kitabu_title": "FARM BOOK - Auto Calculate", "jina": "Farmer Name",
                "shamba": "Farm Name", "tarehe": "Date", "total_pick": "Total Harvest Today (e.g. 150)",
                "what_to_enter": "What are you entering? Choose one:", "enter_ripe": "Enter Ripe Berries Kg (e.g. 140)",
                "enter_dried": "Enter Dried Berries Kg (e.g. 10)", "save": "SAVE RECORD",
                "data_title": "All Farm Data - Search & Edit", "graphs_title": "Harvest Graphs",
                "download": "Download CSV", "harvest_title": "Harvest", "money_title": "Money",
                "input_hint": "Enter number", "auto_label": "Auto", "total_label": "TOTAL",
                "search_hint": "Search farmer or farm...", "delete_last": "Delete Last", "clear_all": "Clear All Data",
                "weather_title": "KIAMBU WEATHER - Farm Advice", "weather_sub": "When to prune, fertilize, harvest",
                "moon_title": "MOON CALENDAR - Coffee Planting by Moon", "moon_sub": "Old wisdom for best harvest",
                "tab_farm": "FARM BOOK", "tab_forecast": "FORECAST"},
    "Kiswahili": {"app_title": "MASHAMBA YA KAHAWA KIAMBU", "slogan": "Kahawa yetu mapato bora", "login_title": "Ingia",
                  "name": "Jina Lako", "password": "Nenosiri", "enter": "INGIA", "profile_title": "WASIFU WA MKULIMA",
                  "my_profile": "Wasifu Wangu", "farmer_label": "Mkulima wa Kahawa Kiambu", "logout": "Toka",
                  "current_prices": "BEI ZA SASA", "ripe_kg_label": "Kahawa Mbivu / KG",
                  "dried_kg_label": "Mbuni Kavu / KG", "ripe_display": "Kahawa Mbivu", "dried_display": "Mbuni Kavu",
                  "ripe_plain": "Kahawa Mbivu", "dried_plain": "Mbuni Kavu", "total_boxes_title": "Jumla Yote",
                  "kilos": "KILO", "pesa": "PESA", "total": "JUMLA YA MAPATO", "jumla_kg": "kg jumla",
                  "kitabu_title": "KITABU - Hesabu Kiotomatiki", "jina": "Jina la Mkulima", "shamba": "Shamba",
                  "tarehe": "Tarehe", "total_pick": "Jumla ya Mavuno Leo (mfano 150)",
                  "what_to_enter": "Unaingiza aina gani? Chagua:", "enter_ripe": "Weka Kahawa Mbivu Kg (mfano 140)",
                  "enter_dried": "Weka Mbuni Kavu Kg (mfano 10)", "save": "HIFADHI",
                  "data_title": "Data Yote - Tafuta & Hariri", "graphs_title": "Grafu za Mavuno",
                  "download": "Pakua CSV", "harvest_title": "Mavuno", "money_title": "Pesa",
                  "input_hint": "Weka nambari", "auto_label": "Kiotomatiki", "total_label": "JUMLA",
                  "search_hint": "Tafuta mkulima au shamba...", "delete_last": "Futa ya Mwisho",
                  "clear_all": "Futa Data Yote", "weather_title": "HALI YA HEWA KIAMBU - Ushauri wa Shamba",
                  "weather_sub": "Wakati wa kukata, mbolea, kuvuna",
                  "moon_title": "KALENDA YA MWEZI - Kupanda kwa Mwezi", "moon_sub": "Hekima ya zamani kwa mavuno bora",
                  "tab_farm": "KITABU CHA SHAMBA", "tab_forecast": "UTABIRI"},
    "Gikuyu": {"app_title": "MIGUNDA YA KAHAWA KIAMBU", "slogan": "Kahawa yakwa indo njega muno",
               "login_title": "Tonya Ndani", "name": "Riitwa Riaku", "password": "Kihitho", "enter": "TONYA",
               "profile_title": "MURIMI PROFILE", "my_profile": "Profile Yakwa",
               "farmer_label": "Murimi wa Kahawa Kiambu", "logout": "Uma", "current_prices": "MITENGO YA UMUTHI",
               "ripe_kg_label": "Kahawa Njeku / KG", "dried_kg_label": "Mbuni / KG", "ripe_display": "Kahawa Njeku",
               "dried_display": "Mbuni", "ripe_plain": "Kahawa Njeku", "dried_plain": "Mbuni",
               "total_boxes_title": "Kiigana Giothe", "kilos": "KIRO", "pesa": "MBECA", "total": "MBECA YOTHE",
               "jumla_kg": "kg ciothe", "kitabu_title": "KITABU - Kwigana Auto", "jina": "Riitwa", "shamba": "Mugunda",
               "tarehe": "Muthenya", "total_pick": "Magetha ma Umuthi Mothe (ta 150)",
               "what_to_enter": "Ni kii urenda kwikira? Thura kimwe:", "enter_ripe": "Ikira Kahawa Njeku (ta 140)",
               "enter_dried": "Ikira Mbuni (ta 10)", "save": "IGIKIRA / BIKA",
               "data_title": "Data Ciothe - Cuthia & Hariri", "graphs_title": "Mibango ya Magetha",
               "download": "Ruta CSV", "harvest_title": "Magetha", "money_title": "Mbeca", "input_hint": "Ikira namba",
               "auto_label": "Kwigana", "total_label": "Hamwe", "search_hint": "Cuthia murimi kana mugunda...",
               "delete_last": "Ruta ya Mwisho", "clear_all": "Ruta Data Ciothe",
               "weather_title": "RURU RWA KIAMBU - Utaaro wa Mugunda",
               "weather_sub": "Ihinda ria guthinja, thumu, kutha", "moon_title": "KALENDA YA MWERI - Kuhanda na Mweri",
               "moon_sub": "Ugi wa tene niundu wa magetha mega", "tab_farm": "KITABU KIA MUGUNDA",
               "tab_forecast": "UTABIRI"}
}


def t(k): return LANG[st.session_state.lang].get(k, k)


def login_page():
    st.markdown(
        f"""<div style="background: linear-gradient(90deg, #7f1d1d, #dc2626); padding:25px; border-radius:20px; text-align:center; color:white; border:4px solid #FFD700;"><h1 style="color:white; font-size:36px !important;">☕ {t('app_title')} ☕</h1><p style="color:#A5D6A7;">{t('slogan')}</p></div>""",
        unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🇬🇧 ENGLISH", width='stretch'): st.session_state.lang = "English"; st.rerun()
    with c2:
        if st.button("🇰🇪 KISWAHILI", width='stretch'): st.session_state.lang = "Kiswahili"; st.rerun()
    with c3:
        if st.button("🌿 GIKUYU", width='stretch'): st.session_state.lang = "Gikuyu"; st.rerun()
    login_tab = t("login_title")
    reg_tab = "REGISTER - First Time?" if st.session_state.lang == "English" else "JISAJILI - Mara ya Kwanza?" if st.session_state.lang == "Kiswahili" else "IYANDIKISHE - Ria Mbere?"
    tab_login, tab_register = st.tabs([f"🔐 {login_tab}", f"📝 {reg_tab}"])
    with tab_login:
        st.markdown(f"<div class='white-title'>🔐 {t('login_title')}</div>", unsafe_allow_html=True)
        with st.form("login_form"):
            name = st.text_input("👤 " + t("name"), placeholder="Kitonyi")
            pwd = st.text_input("🔑 " + t("password"), type="password", placeholder="Password")
            if st.form_submit_button("🚀 " + t("enter"), width='stretch', type="primary"):
                if name in st.session_state.users and st.session_state.users[name]["password"] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.username = name
                    st.rerun()
                else:
                    st.error("❌ Wrong! / Kosa! / Makosa!")
    with tab_register:
        st.markdown(f"<div class='white-title'>🌱 {reg_tab}</div>", unsafe_allow_html=True)
        with st.form("register_form"):
            new_name = st.text_input("👤 " + (
                "Name *" if st.session_state.lang == "English" else "Jina *" if st.session_state.lang == "Kiswahili" else "Riitwa *"),
                                     placeholder="Wanjiku")
            new_farm = st.text_input("🌿 " + (
                "Farm *" if st.session_state.lang == "English" else "Shamba *" if st.session_state.lang == "Kiswahili" else "Mugunda *"),
                                     placeholder="Mugunda 2")
            new_phone = st.text_input("📞 " + (
                "Phone *" if st.session_state.lang == "English" else "Simu *" if st.session_state.lang == "Kiswahili" else "Thimu *"),
                                      placeholder="07XXXXXXXX")
            new_pwd = st.text_input("🔑 " + (
                "Password *" if st.session_state.lang == "English" else "Nenosiri *" if st.session_state.lang == "Kiswahili" else "Kihitho *"),
                                    type="password")
            confirm_pwd = st.text_input("🔑 " + (
                "Confirm *" if st.session_state.lang == "English" else "Thibitisha *" if st.session_state.lang == "Kiswahili" else "Kirikania *"),
                                        type="password")
            btn_text = "✅ REGISTER" if st.session_state.lang == "English" else "✅ JISAJILI" if st.session_state.lang == "Kiswahili" else "✅ IYANDIKISHE"
            if st.form_submit_button(btn_text, width='stretch', type="primary"):
                if not all([new_name, new_farm, new_phone, new_pwd]):
                    st.error("❌ Fill all!")
                elif new_pwd != confirm_pwd:
                    st.error("❌ Password mismatch!")
                elif new_name in st.session_state.users:
                    st.error("❌ Exists! Login")
                elif len(new_phone) < 10:
                    st.error("❌ Phone 10 digits")
                else:
                    st.session_state.users[new_name] = {"password": new_pwd, "farm": new_farm, "phone": new_phone}
                    st.success(f"✅ {new_name} Registered!")
                    st.balloons()


if not st.session_state.logged_in:
    login_page()
    st.stop()

with st.sidebar:
    user_info = st.session_state.users.get(st.session_state.username, {})
    raw_farm = user_info.get('farm', '1')
    farm_display = translate_farm_name(raw_farm, st.session_state.lang)
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border: 3px solid white; border-radius: 18px; padding: 18px; text-align: center;">
        <div style="font-size:50px;">👨‍🌾</div>
        <div style="font-size:22px; font-weight:900; color:white; text-shadow:2px 2px 4px black;">{t('profile_title')}</div>
        <div style="font-size:18px; color:white; background: rgba(220,38,38,0.8); padding:8px; border-radius:10px; margin:8px 0; border:2px solid white;">{t('my_profile')}</div>
        <div style="font-size:24px; font-weight:900; color:white; text-shadow:3px 3px 6px black;">{st.session_state.username}</div>
        <div style="font-size:13px; color:#FFCDD2;">{t('farmer_label')}</div>
        <div style="font-size:12px; color:white; margin-top:10px; background: rgba(0,0,0,0.4); padding:6px; border-radius:8px;">📞 {user_info.get('phone', '')} | {farm_display}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t("logout"), width='stretch'):
        st.session_state.logged_in = False
        st.rerun()
    st.divider()
    st.markdown(
        f"<div style='background: rgba(0,0,0,0.3); border:3px solid white; border-radius:12px; padding:12px; text-align:center;'><div style='font-size:20px; font-weight:900; color:white;'>💰 {t('current_prices')}</div></div>",
        unsafe_allow_html=True)
    price_ripe = st.number_input(f"🍒 {t('ripe_kg_label')}", value=120, step=5)
    price_dried = st.number_input(f"🟤 {t('dried_kg_label')}", value=60, step=5)

st.markdown(
    f"""<div style="background: linear-gradient(90deg, #0B3D2E, #2E7D32); padding:25px; border-radius:18px; text-align:center; color:white; border:4px solid #81C784;"><h2 style="margin:0; color:white; font-size:36px !important;">{t('app_title')}</h2><p style="margin:8px 0 0 0; font-size:22px !important; font-weight:bold; font-style:italic; color:#C8E6C9;">"{t('slogan')}"</p></div>""",
    unsafe_allow_html=True)
st.markdown(
    f"""<div style="display:flex; gap:15px; justify-content:center; margin:15px 0; flex-wrap:wrap;"><div style="background: #dc2626; color:white; padding:15px 30px; border-radius:12px; font-weight:900; font-size:24px !important; border:3px solid white;">🍒 {t('ripe_display')}: KSH {price_ripe}</div><div style="background: #5D3311; color:white; padding:15px 30px; border-radius:12px; font-weight:900; font-size:24px !important; border:3px solid white;">🟤 {t('dried_display')}: KSH {price_dried}</div></div>""",
    unsafe_allow_html=True)

st.markdown('<div class="main-tabs">', unsafe_allow_html=True)
tab_farm, tab_forecast = st.tabs([f"📖 {t('tab_farm')}", f"🌦️ {t('tab_forecast')}"])
st.markdown('</div>', unsafe_allow_html=True)

with tab_farm:
    df = pd.DataFrame(st.session_state.kitabu)
    ripe_df = df[df["Aina"] == "Ripe Berries"] if len(df) > 0 else pd.DataFrame()
    dried_df = df[df["Aina"] == "Dried Berries"] if len(df) > 0 else pd.DataFrame()
    ripe_kgs_total = ripe_df['Kilos'].sum() if len(df) > 0 else 0
    dried_kgs_total = dried_df['Kilos'].sum() if len(df) > 0 else 0
    ripe_pesa_total = ripe_df['Pesa'].sum() if len(df) > 0 else 0
    dried_pesa_total = dried_df['Pesa'].sum() if len(df) > 0 else 0
    total_pesa = df['Pesa'].sum() if len(df) > 0 else 0

    st.markdown(f"### {t('total_boxes_title')}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div class="big-card" style="border-color: #dc2626;"><div style="font-size:24px; font-weight:bold; color:#dc2626;">🍒 {t('ripe_display')}</div><div style="font-size:38px; font-weight:900; color:black;">{ripe_kgs_total:,.1f} kg</div><div style="font-size:14px; color:#666;">{len(ripe_df)} records</div></div>""",
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"""<div class="big-card" style="border-color: #5D3311;"><div style="font-size:24px; font-weight:bold; color:#5D3311;">🟤 {t('dried_display')}</div><div style="font-size:38px; font-weight:900; color:black;">{dried_kgs_total:,.1f} kg</div><div style="font-size:14px; color:#666;">{len(dried_df)} records</div></div>""",
            unsafe_allow_html=True)
    st.write("")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            f"""<div class="big-card" style="border-color: #dc2626; background:#FFF5F5;"><div style="font-size:20px; color:#dc2626;">🍒 {t('ripe_display')} {t('pesa')}</div><div style="font-size:32px; font-weight:900; color:black;">KSH {ripe_pesa_total:,.0f}</div></div>""",
            unsafe_allow_html=True)
    with c4:
        st.markdown(
            f"""<div class="big-card" style="border-color: #5D3311; background:#FFF8F0;"><div style="font-size:20px; color:#5D3311;">🟤 {t('dried_display')} {t('pesa')}</div><div style="font-size:32px; font-weight:900; color:black;">KSH {dried_pesa_total:,.0f}</div></div>""",
            unsafe_allow_html=True)
    st.write("")
    st.markdown(
        f"""<div class="big-card" style="border-color: #FFD700; background: linear-gradient(90deg, #FFFDE7, #FFF9C4);"><div style="font-size:28px; font-weight:900; color:#B45309;">🏆 {t('total')}</div><div style="font-size:16px; color:#666;">{ripe_kgs_total + dried_kgs_total:,.1f} {t('jumla_kg')} | {len(df)} records</div><div style="font-size:44px; font-weight:900; color:#0B3D2E;">KSH {total_pesa:,.0f}</div></div>""",
        unsafe_allow_html=True)

    st.divider()
    st.subheader(t("kitabu_title"))
    st.markdown(f"<div class='white-title'>📝 {t('jina')}</div>", unsafe_allow_html=True)
    farmer = st.text_input("", value=st.session_state.username, placeholder=t("input_hint"),
                           label_visibility="collapsed", key="farmer_input")
    st.markdown(f"<div class='white-title'>🌿 {t('shamba')}</div>", unsafe_allow_html=True)
    shamba_list = ["Farm 1", "Farm 2", "Farm 3"] if st.session_state.lang == "English" else ["Shamba 1", "Shamba 2",
                                                                                             "Shamba 3"] if st.session_state.lang == "Kiswahili" else [
        "Mugunda 1", "Mugunda 2", "Mugunda 3"]
    default_farm = st.session_state.users.get(st.session_state.username, {}).get('farm', '1')
    if st.session_state.lang == "Kiswahili":
        default_display = f"Shamba {default_farm[-1] if default_farm[-1].isdigit() else '1'}"
    elif st.session_state.lang == "Gikuyu":
        default_display = f"Mugunda {default_farm[-1] if default_farm[-1].isdigit() else '1'}"
    else:
        default_display = f"Farm {default_farm[-1] if default_farm[-1].isdigit() else '1'}"
    shamba = st.selectbox("", shamba_list,
                          index=shamba_list.index(default_display) if default_display in shamba_list else 0,
                          label_visibility="collapsed", key="shamba_input")
    st.markdown(f"<div class='white-title'>📅 {t('tarehe')}</div>", unsafe_allow_html=True)
    tarehe = st.date_input("", value=date.today(), label_visibility="collapsed", key="tarehe_input")
    st.markdown(f"<div class='white-title'>⚖️ {t('total_pick')}</div>", unsafe_allow_html=True)
    total_kgs_str = st.text_input("", value="150", placeholder=t("input_hint"), label_visibility="collapsed",
                                  key="total_input")
    try:
        total_kgs = float(total_kgs_str) if total_kgs_str else 0.0
    except:
        total_kgs = 0.0
    st.markdown(f"<div class='white-title'>❓ {t('what_to_enter')}</div>", unsafe_allow_html=True)
    mode = st.radio("", [f"🍒 {t('ripe_display')}", f"🟤 {t('dried_display')}"], horizontal=True,
                    label_visibility="collapsed", key="mode_input")
    if "Mbivu" in mode or "Njeku" in mode or "Ripe" in mode:
        st.markdown(f"<div class='white-title'>🍒 {t('enter_ripe')}</div>", unsafe_allow_html=True)
        ripe_kgs_str = st.text_input("", value="140" if total_kgs >= 140 else "0", placeholder=t("input_hint"),
                                     label_visibility="collapsed", key="ripe_input")
        try:
            ripe_kgs = float(ripe_kgs_str) if ripe_kgs_str else 0.0
        except:
            ripe_kgs = 0.0
        dried_kgs = total_kgs - ripe_kgs
        if dried_kgs < 0: dried_kgs = 0
        st.markdown(
            f"""<div style="background:#00C853; color:white; padding:15px; border-radius:12px; border:3px solid white; font-weight:900;">🟤 {t('auto_label')}: {t('dried_display')} = {dried_kgs} kg</div>""",
            unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='white-title'>🟤 {t('enter_dried')}</div>", unsafe_allow_html=True)
        dried_kgs_str = st.text_input("", value="10" if total_kgs >= 10 else "0", placeholder=t("input_hint"),
                                      label_visibility="collapsed", key="dried_input")
        try:
            dried_kgs = float(dried_kgs_str) if dried_kgs_str else 0.0
        except:
            dried_kgs = 0.0
        ripe_kgs = total_kgs - dried_kgs
        if ripe_kgs < 0: ripe_kgs = 0
        st.markdown(
            f"""<div style="background:#00C853; color:white; padding:15px; border-radius:12px; border:3px solid white; font-weight:900;">🍒 {t('auto_label')}: {t('ripe_display')} = {ripe_kgs} kg</div>""",
            unsafe_allow_html=True)

    pesa_ripe = ripe_kgs * price_ripe;
    pesa_dried = dried_kgs * price_dried;
    pesa_total = pesa_ripe + pesa_dried
    st.markdown(
        f"""<div style="background:white; padding:15px; border-radius:12px; border:4px solid #00FF00; margin-top:15px;"><p style="color:#dc2626; font-weight:900;">🍒 {t('ripe_display')}: {ripe_kgs}kg x {price_ripe} = KSH {pesa_ripe:,.0f}</p><p style="color:#5D3311; font-weight:900;">🟤 {t('dried_display')}: {dried_kgs}kg x {price_dried} = KSH {pesa_dried:,.0f}</p><p style="color:#0B3D2E; font-weight:900; font-size:26px !important; border-top:2px solid #ccc; padding-top:8px;">🏆 {t('total_label')}: {total_kgs}kg = KSH {pesa_total:,.0f}</p></div>""",
        unsafe_allow_html=True)

    if st.button(t("save"), width='stretch', type="primary"):
        if total_kgs <= 0:
            st.error("Weka / Enter / Ikira!")
        else:
            if ripe_kgs > 0: st.session_state.kitabu.append(
                {"Tarehe": str(tarehe), "Jina": farmer, "Aina": "Ripe Berries", "Shamba": shamba, "Kilos": ripe_kgs,
                 "Bei": price_ripe, "Pesa": pesa_ripe})
            if dried_kgs > 0: st.session_state.kitabu.append(
                {"Tarehe": str(tarehe), "Jina": farmer, "Aina": "Dried Berries", "Shamba": shamba, "Kilos": dried_kgs,
                 "Bei": price_dried, "Pesa": pesa_dried})
            st.success("Saved! / Imehifadhiwa! / Igikiritwo!");
            st.balloons();
            st.rerun()

    st.divider()
    st.subheader(t("data_title"))
    search = st.text_input("🔍", placeholder=t("search_hint"), label_visibility="collapsed", key="search")
    df_display = pd.DataFrame(st.session_state.kitabu)
    if search and len(df_display) > 0:
        df_display = df_display[df_display.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    if len(df_display) > 0:
        if st.session_state.lang == "English":
            col_map = {"Tarehe": "Date", "Jina": "Farmer", "Aina": "Type", "Shamba": "Farm", "Kilos": "Kilos",
                       "Bei": "Price", "Pesa": "Money"}
            df_display["Aina"] = df_display["Aina"].replace(
                {"Ripe Berries": "Ripe Berries", "Dried Berries": "Dried Berries"})
        elif st.session_state.lang == "Kiswahili":
            col_map = {"Tarehe": "Tarehe", "Jina": "Jina", "Aina": "Aina", "Shamba": "Shamba", "Kilos": "Kilo",
                       "Bei": "Bei", "Pesa": "Pesa"}
            df_display["Aina"] = df_display["Aina"].replace(
                {"Ripe Berries": "Kahawa Mbivu", "Dried Berries": "Mbuni Kavu"})
        else:
            col_map = {"Tarehe": "Muthenya", "Jina": "Riitwa", "Aina": "Muthirimo", "Shamba": "Mugunda",
                       "Kilos": "Kiro", "Bei": "Mutengo", "Pesa": "Mbeca"}
            df_display["Aina"] = df_display["Aina"].replace({"Ripe Berries": "Kahawa Njeku", "Dried Berries": "Mbuni"})
        df_display_renamed = df_display.rename(columns=col_map)
        st.dataframe(df_display_renamed, width='stretch', hide_index=True, height=400)
        col_del1, col_del2, col_del3 = st.columns(3)
        with col_del1:
            if st.button(t("delete_last"), width='stretch'):
                if st.session_state.kitabu:
                    st.session_state.kitabu.pop()
                    st.success("Last deleted!")
                    st.rerun()
        with col_del2:
            if st.button(t("clear_all"), width='stretch'):
                st.session_state.kitabu = []
                st.success("All cleared!")
                st.rerun()
        with col_del3:
            st.download_button(t("download"), df_display_renamed.to_csv(index=False).encode('utf-8'),
                               "kiambu_coffee.csv", "text/csv", width='stretch')
    else:
        st.info("No data yet - Add records!")

    st.divider()
    st.subheader(t("graphs_title"))
    df_graph = pd.DataFrame(st.session_state.kitabu)
    if len(df_graph) > 0:
        def map_aina(a):
            return t("ripe_plain") if "Ripe" in a else t("dried_plain")


        df_graph["Aina_Translated"] = df_graph["Aina"].apply(map_aina)
        fig1 = px.bar(df_graph, x="Tarehe", y="Kilos", color="Aina_Translated", barmode="group",
                      color_discrete_map={t("ripe_plain"): "#dc2626", t("dried_plain"): "#5D3311"},
                      title=t("harvest_title"))
        fig1.update_layout(font=dict(size=18), height=450, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="white")
        fig2 = px.pie(df_graph, values="Pesa", names="Aina_Translated",
                      color_discrete_map={t("ripe_plain"): "#dc2626", t("dried_plain"): "#5D3311"},
                      title=t("money_title"))
        fig2.update_layout(font=dict(size=18), height=450, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        c1g, c2g = st.columns(2)
        with c1g:
            st.plotly_chart(fig1, width='stretch')
        with c2g:
            st.plotly_chart(fig2, width='stretch')
    else:
        st.info("No graphs - Add data first!")

with tab_forecast:
    st.subheader(f"🌦️ {t('weather_title')}")
    st.markdown(f"<p style='color:white; font-style:italic;'>{t('weather_sub')}</p>", unsafe_allow_html=True)
    weather_data = get_kiambu_weather()
    if weather_data:
        daily = weather_data['daily']
        dates = daily['time'];
        tmax = daily['temperature_2m_max'];
        tmin = daily['temperature_2m_min'];
        precip = daily['precipitation_sum'];
        prob = daily.get('precipitation_probability_max', [0] * 7);
        wind = daily.get('wind_speed_10m_max', [0] * 7)
        cols = st.columns(4)
        for i in range(min(7, len(dates))):
            d = datetime.strptime(dates[i], "%Y-%m-%d")
            day_name = get_day_name_translated(d, st.session_state.lang)
            advice = get_farm_advice(precip[i], tmax[i], st.session_state.lang)
            icon = "🌧️" if precip[i] > 10 else "🌦️" if precip[i] > 2 else "☀️"
            if i > 0 and i % 4 == 0:
                st.write("")
                cols = st.columns(4)
            with cols[i % 4]:
                st.markdown(f"""
                <div class="weather-card">
                    <div style="font-weight:900; font-size:12px; color:#0B3D2E;">{day_name}</div>
                    <div style="font-size:40px;">{icon}</div>
                    <div style="font-size:13px; color:#333;">{tmin[i]:.0f}° - {tmax[i]:.0f}°C</div>
                    <div style="font-size:16px; font-weight:900; color:#1565C0;">💧 {precip[i]:.1f} mm</div>
                    <div style="font-size:11px; color:#666;">{prob[i]}% | 💨 {wind[i]:.0f} km/h</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<div class='weather-advice'>{advice}</div>", unsafe_allow_html=True)
        total_rain = sum(precip);
        avg_temp = sum(tmax) / len(tmax)
        if total_rain > 30:
            week_advice = "🌧️ Wet week! DO FERTILIZER! Don't prune" if st.session_state.lang == "English" else "🌧️ Wiki ya mvua! WEKA MBOLEA! Usikate" if st.session_state.lang == "Kiswahili" else "🌧️ Kiumia kia mbua! IKIRA THUMU! Ndugathinje"
        elif total_rain < 10:
            week_advice = "☀️ Dry week! BEST FOR PRUNING & HARVEST!" if st.session_state.lang == "English" else "☀️ Wiki kavu! BORA KWA KUKATA & KUVUNA!" if st.session_state.lang == "Kiswahili" else "☀️ Kiumia kiumu! KIGO KWA GUTHINJA & KUTHA!"
        else:
            week_advice = "🌦️ Mixed week! Fertilizer early, prune later" if st.session_state.lang == "English" else "🌦️ Wiki ya mchanganyiko! Mbolea mwanzoni, kata baadaye" if st.session_state.lang == "Kiswahili" else "🌦️ Kiumia kia mbua na riua! Thumu mbere, thinja thuutha"
        st.markdown(
            f"""<div style="background: linear-gradient(90deg, #FFD700, #FFEB3B); padding:20px; border-radius:15px; border:4px solid #0B3D2E; margin-top:15px; text-align:center;"><div style="font-size:18px; font-weight:900; color:#0B3D2E;">📅 WEEK: Avg {avg_temp:.0f}°C, Total {total_rain:.0f}mm</div><div style="font-size:16px; color:#333; margin-top:10px; font-weight:bold;">{week_advice}</div></div>""",
            unsafe_allow_html=True)
    else:
        st.warning("⚠️ Weather loading... Using Kiambu average")
        st.markdown(
            """<div style="background:white; padding:15px; border-radius:12px;"><p style="color:black; font-weight:bold;">🌦️ KIAMBU GENERAL:</p><p style="color:#333;">☀️ Jan-Mar, Jul-Sep (Dry): PRUNE, HARVEST, SPRAY</p><p style="color:#333;">🌧️ Mar-May, Oct-Dec (Rainy): FERTILIZER, PLANTING</p></div>""",
            unsafe_allow_html=True)

    st.divider()
    st.subheader(f"🌙 {t('moon_title')}")
    st.markdown(f"<p style='color:#FFD700; font-style:italic; font-weight:bold;'>{t('moon_sub')}</p>",
                unsafe_allow_html=True)
    today = datetime.now()
    moon_cols = st.columns(4)
    for i in range(8):
        d = today + timedelta(days=i)
        phase = moon_phase_on_date(d)
        icon, name, advice, coffee_action = moon_icon_and_name(phase, st.session_state.lang)
        day_str = get_day_name_translated(d, st.session_state.lang)
        if i > 0 and i % 4 == 0:
            st.write("")
            moon_cols = st.columns(4)
        with moon_cols[i % 4]:
            st.markdown(f"""
            <div class="moon-card">
                <div style="font-weight:900; font-size:11px; color:#FFD700;">{day_str}</div>
                <div style="font-size:50px; margin:10px 0;">{icon}</div>
                <div style="font-weight:900; font-size:13px; color:white;">{name}</div>
                <div style="font-size:11px; color:#A5D6A7; margin:5px 0;">{advice}</div>
                <div style="background:#FFD700; color:#1a1a2e; padding:5px 8px; border-radius:8px; font-weight:900; font-size:12px; margin-top:8px;">{coffee_action}</div>
            </div>
            """, unsafe_allow_html=True)
    phase_today = moon_phase_on_date(today)
    icon_today, name_today, advice_today, coffee_today = moon_icon_and_name(phase_today, st.session_state.lang)

    if st.session_state.lang == "Kiswahili":
        guide_text = "🌑 Mwezi Mpia = Panda miche | 🌒 Unakua = Dawa ya majani<br>🌕 Mwezi Mkuu = Vuna matunda tamu | 🌗 Mwisho = BORA KATA, palilia"
    elif st.session_state.lang == "Gikuyu":
        guide_text = "🌑 Mweri Meru = Handa mbeu | 🌒 Urakuura = Guthaambia mathangu<br>🌕 Mweri Munene = Tha matunda irimu | 🌗 Muico = KIGO GUTHINJA"
    else:
        guide_text = "🌑 New Moon = Plant seedlings | 🌒 Waxing = Foliar spray, growth<br>🌕 Full Moon = Harvest ripe, juicy berries | 🌗 Last Quarter = BEST PRUNE, weed, pest control"

    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1a1a2e, #16213e); padding:20px; border-radius:15px; border:4px solid #FFD700; margin-top:20px; text-align:center;">
        <div style="font-size:20px; font-weight:900; color:#FFD700;">🌙 TODAY: {icon_today} {name_today} - {coffee_today}</div>
        <div style="font-size:14px; color:white; margin-top:10px;">{advice_today}</div>
        <div style="font-size:12px; color:#A5D6A7; margin-top:10px; background: rgba(255,255,255,0.1); padding:10px; border-radius:8px;">
            {guide_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
