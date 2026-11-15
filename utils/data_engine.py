import pandas as pd
import numpy as np

def load_earth_datasets():
    """
    Generates and returns curated NASA Earth Information Center (EIC) style
    multi-decade datasets for Greenhouse Gases, Global Temperature Anomalies,
    Sea Level Rise, and Arctic Sea Ice Extent.
    """
    years = np.arange(1980, 2027)
    n = len(years)
    np.random.seed(42)

    # CO2 (ppm) - Keeling Curve trend
    co2 = 338.7 + 1.55 * (years - 1980) + 0.014 * (years - 1980)**2 + np.random.normal(0, 0.35, n)
    # Methane CH4 (ppb)
    ch4 = 1565.0 + 7.2 * (years - 1980) + 0.04 * (years - 1980)**2 + np.random.normal(0, 4.5, n)
    # Global Surface Temp Anomaly (C relative to 1951-1980 baseline)
    temp_anomaly = 0.22 + 0.019 * (years - 1980) + 0.00018 * (years - 1980)**2 + np.random.normal(0, 0.08, n)
    # Global Mean Sea Level Change (mm relative to 1993)
    sea_level = -38.0 + 3.1 * (years - 1980) + 0.025 * (years - 1980)**2 + np.random.normal(0, 1.8, n)
    # Arctic Sea Ice Minimum Extent (Million sq km)
    arctic_ice = 7.55 - 0.078 * (years - 1980) + np.random.normal(0, 0.32, n)

    df = pd.DataFrame({
        "Year": years,
        "CO2_ppm": np.round(co2, 2),
        "CH4_ppb": np.round(ch4, 1),
        "Temp_Anomaly_C": np.round(temp_anomaly, 3),
        "Sea_Level_mm": np.round(sea_level, 1),
        "Arctic_Ice_Mkm2": np.round(arctic_ice, 2)
    })
    return df

def get_global_stations():
    """Returns NASA EIC / AERONET / OCO-2 global observation nodes."""
    stations = [
        {"Station": "Mauna Loa Observatory (MLO)", "Lat": 19.5362, "Lon": -155.5763, "Region": "Pacific Ocean", "CO2_ppm": 426.8, "Temp_Anomaly": "+1.28°C", "Status": "Nominal"},
        {"Station": "Ny-Ålesund Arctic Station", "Lat": 78.9235, "Lon": 11.9222, "Region": "Svalbard, Arctic", "CO2_ppm": 429.4, "Temp_Anomaly": "+3.45°C", "Status": "Critical Warming"},
        {"Station": "Amazon Tall Tower Observatory (ATTO)", "Lat": -2.1459, "Lon": -59.0056, "Region": "Amazon Basin", "CO2_ppm": 424.1, "Temp_Anomaly": "+1.52°C", "Status": "Carbon Flux Alert"},
        {"Station": "Barrow Atmospheric Baseline", "Lat": 71.3230, "Lon": -156.6114, "Region": "Alaska, USA", "CO2_ppm": 428.9, "Temp_Anomaly": "+3.12°C", "Status": "Active Telemetry"},
        {"Station": "Cape Grim Baseline Station", "Lat": -40.6833, "Lon": 144.6833, "Region": "Tasmania, Australia", "CO2_ppm": 421.2, "Temp_Anomaly": "+1.04°C", "Status": "Nominal"},
        {"Station": "South Pole Observatory (SPO)", "Lat": -89.9970, "Lon": -24.8000, "Region": "Antarctica", "CO2_ppm": 420.5, "Temp_Anomaly": "+0.95°C", "Status": "Nominal"},
        {"Station": "Izana Atmospheric Observatory", "Lat": 28.3090, "Lon": -16.4994, "Region": "Tenerife, Atlantic", "CO2_ppm": 425.7, "Temp_Anomaly": "+1.39°C", "Status": "Active Telemetry"},
    ]
    return pd.DataFrame(stations)
