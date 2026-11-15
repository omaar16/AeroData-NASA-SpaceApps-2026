# 🛰️ AeroData: The Earth Information Jukebox
**NASA International Space Apps Challenge 2026**
**Challenge Track:** *The Earth Information Jukebox*

## Overview
**AeroData** transforms multi-decade NASA Earth Information Center (EIC) datasets—including atmospheric $\text{CO}_2$, methane ($\text{CH}_4$), global surface temperature anomalies, sea level rise, and Arctic sea ice extent—into an interactive visual and acoustic experience (**Data Sonification**).

By translating environmental telemetry into harmonic musical scales and downloadable `.WAV` audio tracks, AeroData enables researchers, students, and the public to both *see* and *hear* how our planet is changing.

## Key Features
- **Interactive Data Sonification Engine (`utils/sonification.py`):** Maps climate indicators to harmonic scales (C Major Pentatonic, A Minor Ambient, Lydian Space Synth, and Continuous Telemetry Sweep) using additive synthesis.
- **NASA Earth Telemetry Explorer (`utils/data_engine.py`):** Multi-decade climate datasets (1980–2026) and global observation nodes.
- **Audio Export:** Download generated climate symphonies directly as `.WAV` files.
- **Geospatial Telemetry Map:** Interactive Plotly visualization of global atmospheric monitoring stations.

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```
