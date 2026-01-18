import ee
import pandas as pd

# Initialize Earth Engine
ee.Initialize(project="climate-ee")

# -----------------------------
# Parameters
# -----------------------------
START_DATE = "2021-01-01"
END_DATE = "2024-12-31"
OUTPUT_CSV = "outputs/humidity_lga_monthly_benue.csv"

# -----------------------------
# Load Benue LGAs
# -----------------------------
lgas = ee.FeatureCollection("FAO/GAUL/2015/level2") \
    .filter(ee.Filter.eq("ADM1_NAME", "Benue"))

# -----------------------------
# ERA5-Land Monthly Aggregated
# -----------------------------
era5 = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR") \
    .filterDate(START_DATE, END_DATE)

# -----------------------------
# Relative Humidity calculation
# -----------------------------
def compute_rh(img):
    t = img.select("temperature_2m").subtract(273.15)
    td = img.select("dewpoint_temperature_2m").subtract(273.15)

    es = t.expression(
        "6.112 * exp((17.67 * T) / (T + 243.5))",
        {"T": t}
    )

    e = td.expression(
        "6.112 * exp((17.67 * Td) / (Td + 243.5))",
        {"Td": td}
    )

    rh = e.divide(es).multiply(100).rename("relative_humidity")

    return rh.set("date", img.date().format("YYYY-MM"))

# Apply RH computation
rh_collection = era5.map(compute_rh)

# -----------------------------
# LGA-level reduction
# -----------------------------
def reduce_lga(img):
    date = img.get("date")

    reduced = img.reduceRegions(
        collection=lgas,
        reducer=ee.Reducer.mean(),
        scale=10000
    )

    return reduced.map(lambda f: f.set("date", date))

# Flatten results
results = rh_collection.map(reduce_lga).flatten()

# -----------------------------
# Export to CSV locally
# -----------------------------
features = results.getInfo()["features"]

rows = [{
    "date": f["properties"]["date"],
    "lga": f["properties"]["ADM2_NAME"],
    "relative_humidity_percent": f["properties"]["mean"]
} for f in features]

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved LGA-level humidity data to {OUTPUT_CSV}")
