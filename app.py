import streamlit as st
from views import eda, analysis, dashboard, about, preprocessing

st.set_page_config(
    page_title='IFest 2022 Universitas Padjajaran - Archanexus Team',
    page_icon='https://telkomuniversity.ac.id/wp-content/uploads/2019/07/cropped-favicon-2-32x32.png',
    layout='wide'
)

PAGES = {
    "🏠 Dashboard": dashboard,
    "🔍 Eksplorasi Dataset": eda,
    "🧹 Pra-pemrosesan Dataset": preprocessing,
    "💡 Analisis Dataset": analysis,
    "👥 Tentang Kami": about,
}

st.sidebar.image("static/image/logopurple.png", width=150)
st.sidebar.header('IFEST 2022 - DAC - Archanexus')

page = st.sidebar.selectbox("Pindah Halaman", list(PAGES.keys()))
page = PAGES[page]
page.app()