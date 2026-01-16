import ee

# Initialize Earth Engine with registered project
ee.Initialize(project="climate-ee")

# -------------------------------
# 1. Load Benue LGAs
# -------------------------------
# GAUL level 2 = Local Government Areas
lgas = (
    ee.FeatureCollection("FAO/GAUL/2015/level2")
    .filter(ee.Filter.eq("ADM0_NAME", "Nigeria"))
    .filter(ee.Filter.eq("ADM1_NAME", "Benue"))
)

# -------------------------------
# 2. Load MODIS NDVI
# -------------------------------
ndvi_ic = (
    ee.ImageCollection("MODIS/061/MOD13Q1")
    .select("NDVI")
)

# -------------------------------
# 3. Create monthly NDVI composites
# -------------------------------
def monthly_ndvi(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, "month")

    ndvi = (
        ndvi_ic
        .filterDate(start, end)
        .mean()
        .multiply(0.0001)  # MODIS NDVI scale factor
        .set({
            "year": year,
            "month": month,
            "date": start.format("YYYY-MM")
        })
    )

    return ndvi


# Create list of months (Jan 2021 – Dec 2024)
years = ee.List.sequence(2021, 2024)
months = ee.List.sequence(1, 12)

monthly_images = ee.ImageCollection(
    years.map(
        lambda y: months.map(
            lambda m: monthly_ndvi(ee.Number(y), ee.Number(m))
        )
    ).flatten()
)

# -------------------------------
# 4. Reduce NDVI by LGA
# -------------------------------
def reduce_by_lga(image):
    stats = image.reduceRegions(
        collection=lgas,
        reducer=ee.Reducer.mean(),
        scale=250  # MODIS resolution
    )

    return stats.map(
        lambda f: f.set({
            "year": image.get("year"),
            "month": image.get("month"),
            "date": image.get("date")
        })
    )


ndvi_lga_table = monthly_images.map(reduce_by_lga).flatten()

# -------------------------------
# 5. Export to Google Drive
# -------------------------------
task = ee.batch.Export.table.toDrive(
    collection=ndvi_lga_table,
    description="Benue_LGA_Monthly_NDVI_2021_2024",
    folder="EarthEngine",
    fileNamePrefix="benue_lga_monthly_ndvi_2021_2024",
    fileFormat="CSV"
)

task.start()

print("Export task started successfully.")
