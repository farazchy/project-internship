%pyspark
from pyspark.sql import functions as F

# 1️⃣ Clean dataset: Remove invalid fares & null airline names
df_cleaned = df.filter(
    (F.col("totalFare").isNotNull()) & 
    (F.col("totalFare") > 0) & 
    (F.col("segmentsAirlineName").isNotNull())
).withColumn(
    "cleanedAirlineName", F.split(F.col("segmentsAirlineName"), "\|\|").getItem(0)
)

# 2️⃣ Handle null values in airline names by replacing them with "Unknown"
df_cleaned = df_cleaned.fillna({"cleanedAirlineName": "Unknown"})

# 3️⃣ Compute flight count & average fare for each airline
popular_airlines = df_cleaned.groupBy("cleanedAirlineName") \
    .agg(
        F.count("legId").alias("Total_Flights"),
        F.round(F.avg("totalFare"), 2).alias("Avg_Fare")
    ) \
    .orderBy(F.col("Total_Flights").desc())

# 4️⃣ Show results
print("📌 Improved Airline Ranking:")
popular_airlines.show(20, truncate=False)
