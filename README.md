# Spatiotemporal Climate–Health Modeling

This repository contains **research-ready workflows** for deriving spatiotemporal environmental indicators from satellite data for climate and health research.

The current focus is on generating **monthly NDVI summaries across Local Government Areas (LGAs) in Benue State, Nigeria**, using **Google Earth Engine (GEE)** and Python. This is part of a climate variability and malaria modeling project.

---

## Project Objectives
- Derive **monthly NDVI** from satellite imagery (MODIS, 2021–2024)  
- Aggregate NDVI at **LGA level**  
- Export clean tabular outputs (CSV) for downstream modeling  
- Support climate variability and malaria risk modeling  

---

## Data Sources
- **NDVI**: MODIS/006/MOD13Q1 via Google Earth Engine  
- **Administrative boundaries**: Benue State LGAs (vector features in GEE)  
- Optional: Rainfall & temperature datasets (pre-processed from MODIS/ERA5)  

---

## Tech Stack
- Python 3.11  
- Google Earth Engine Python API  
- pandas, geopandas (optional for local handling)  
- CSV outputs for modeling and analysis  

---

## Project Structure

├── src/
│ ├── ndvi_lga_monthly.py # Monthly NDVI extraction by LGA
│ ├── rainfall_processing.py # Optional rainfall preprocessing
│ └── malaria_model.py # Optional malaria risk modeling
├── data/ # Optional small datasets / metadata
│ └── README.md
├── docs/ # Additional documentation
├── gee-env/ # Python virtual environment (ignored by git)
├── .gitignore
├── README.md
├── requirements.txt
├── CITATION.cff # Citation metadata for GitHub
└── LICENSE

---

## Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/eluseful/spatiotemporal-climate-health.git
cd spatiotemporal-climate-health
