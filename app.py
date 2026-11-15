import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_engine import load_earth_datasets, get_global_stations
from utils.sonification import generate_jukebox_audio, SCALES

st.set_page_config(
    page_title="AeroData | The Earth Information Jukebox",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Aerospace Dark Theme Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .jukebox-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

df = load_earth_datasets()
stations_df = get_global_stations()

# Sidebar Controls
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg", width=80)
    st.title("AeroData Jukebox")
    st.caption("NASA Space Apps Challenge 2026")
    st.divider()

    year_range = st.slider(
        "Select Telemetry Era (Years)",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (1985, 2026)
    )

    dataset_choice = st.selectbox(
        "Earth Information Track",
        [
            "CO2_ppm",
            "Temp_Anomaly_C",
            "Sea_Level_mm",
            "Arctic_Ice_Mkm2",
            "CH4_ppb"
        ],
        format_func=lambda x: {
            "CO2_ppm": "Atmospheric CO₂ Concentration (ppm)",
            "Temp_Anomaly_C": "Global Surface Temperature Anomaly (°C)",
            "Sea_Level_mm": "Global Mean Sea Level Rise (mm)",
            "Arctic_Ice_Mkm2": "Arctic Sea Ice Minimum Extent (M km²)",
            "CH4_ppb": "Atmospheric Methane CH₄ (ppb)"
        }[x]
    )

    scale_choice = st.selectbox("Jukebox Musical Scale", list(SCALES.keys()))
    tempo = st.slider("Note Duration (Seconds / Year)", 0.08, 0.35, 0.16, 0.02)
    st.divider()
    st.info("Built by AeroData for **The Earth Information Jukebox** challenge.")

filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# Header
st.markdown('<div class="main-header">🛰️ AeroData: The Earth Information Jukebox</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transforming NASA Earth Science Telemetry into Interactive Visual & Acoustic Experiences</div>', unsafe_allow_html=True)

# Top KPI Metrics
latest = filtered_df.iloc[-1]
earliest = filtered_df.iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("CO₂ Level", f"{latest['CO2_ppm']} ppm", f"+{latest['CO2_ppm'] - earliest['CO2_ppm']:.1f} ppm")
col2.metric("Temp Anomaly", f"+{latest['Temp_Anomaly_C']} °C", f"+{latest['Temp_Anomaly_C'] - earliest['Temp_Anomaly_C']:.2f} °C")
col3.metric("Sea Level Change", f"{latest['Sea_Level_mm']} mm", f"+{latest['Sea_Level_mm'] - earliest['Sea_Level_mm']:.1f} mm")
col4.metric("Arctic Ice Extent", f"{latest['Arctic_Ice_Mkm2']} M km²", f"{latest['Arctic_Ice_Mkm2'] - earliest['Arctic_Ice_Mkm2']:.2f} M km²")

tab1, tab2, tab3 = st.tabs([
    "🎵 Earth Information Jukebox (Sonification)",
    "🌍 Global Telemetry & Orbital Nodes",
    "📊 Multi-Variable Climate Correlations"
])

with tab1:
    st.subheader("Listen to Earth's Changing Symphony")
    st.write("Each data point in your selected NASA Earth Information track is mapped to harmonic frequencies so you can **hear** climate trends alongside visual telemetry.")

    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.area(
            filtered_df,
            x="Year",
            y=dataset_choice,
            title=f"Selected Jukebox Track: {dataset_choice} ({year_range[0]}–{year_range[1]})",
            markers=True,
            color_discrete_sequence=["#38bdf8"]
        )
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="jukebox-card">', unsafe_allow_html=True)
        st.markdown("### 🎧 Jukebox Deck")
        st.write(f"**Track:** `{dataset_choice}`")
        st.write(f"**Scale:** {scale_choice}")
        st.write(f"**Data Points:** {len(filtered_df)} years")

        wav_bytes = generate_jukebox_audio(
            filtered_df[dataset_choice].values,
            scale_name=scale_choice,
            note_duration=tempo
        )
        st.audio(wav_bytes, format="audio/wav")
        st.download_button(
            label="⬇️ Download Sonified Track (.WAV)",
            data=wav_bytes,
            file_name=f"AeroData_Jukebox_{dataset_choice}_{year_range[0]}_{year_range[1]}.wav",
            mime="audio/wav"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Global NASA Earth Observation Stations")
    fig_map = px.scatter_geo(
        stations_df,
        lat="Lat",
        lon="Lon",
        hover_name="Station",
        hover_data=["Region", "CO2_ppm", "Temp_Anomaly", "Status"],
        size="CO2_ppm",
        color="Status",
        projection="natural earth",
        title="Active Atmospheric & Climate Telemetry Nodes"
    )
    fig_map.update_layout(template="plotly_dark", height=480)
    st.plotly_chart(fig_map, use_container_width=True)
    st.dataframe(stations_df, use_container_width=True)

with tab3:
    st.subheader("CO₂ Concentration vs. Global Temperature Anomaly")
    fig_corr = px.scatter(
        filtered_df,
        x="CO2_ppm",
        y="Temp_Anomaly_C",
        color="Year",
        size="Sea_Level_mm" if (filtered_df["Sea_Level_mm"] > 0).all() else None,
        hover_data=["Year", "Arctic_Ice_Mkm2"],
        title="Radiative Forcing Correlation: Atmospheric CO₂ vs. Surface Temperature"
    )
    fig_corr.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig_corr, use_container_width=True)
