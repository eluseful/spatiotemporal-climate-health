import ee
import pandas as pd

# Initialize Earth Engine (uses your registered project)
ee.Initialize(project="climate-ee")

# -----------------------------
# 1. Load Benue LGAs (ADM2)
# -----------------------------
lgas = (
    ee.FeatureCollection("FAO/GAUL/2015/level2")
    .filter(ee.Filter.eq("ADM1_NAME", "Benue"))
)

# -----------------------------
# 2. Load ERA5-Land Monthly Soil Moisture (UPDATED)
# -----------------------------
collection = (
    ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR")
    .select("volumetric_soil_water_layer_1")
    .filterDate("2021-01-01", "2024-12-31")
)

# -----------------------------
# 3. Function: Monthly × LGA extraction
# -----------------------------
def extract_month_lga(image):
    date = image.date()
    year = date.get("year")
    month = date.get("month")

    def per_lga(lga):
        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=lga.geometry(),
            scale=10000,
            maxPixels=1e13
        ).get("volumetric_soil_water_layer_1")

        return ee.Feature(None, {
            "year": year,
            "month": month,
            "lga_name": lga.get("ADM2_NAME"),
            "soil_moisture": value
        })

    return lgas.map(per_lga)

# -----------------------------
# 4. Apply mapping
# -----------------------------
features = collection.map(extract_month_lga).flatten()

# -----------------------------
# 5. Export to pandas DataFrame
# -----------------------------
data = features.getInfo()["features"]
rows = [f["properties"] for f in data]
df = pd.DataFrame(rows)

# -----------------------------
# 6. Save CSV
# -----------------------------
output_path = "outputs/soil_moisture_lga_monthly_benue.csv"
df.to_csv(output_path, index=False)

print(f"Saved LGA-level soil moisture data to {output_path}")
