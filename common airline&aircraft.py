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

# 1.4.1 Most common airlines (based on frequency of segmentsAirlineName)
# Removing duplicates and cleaning airline names by filtering out entries with "||"
most_common_airlines = df_cleaned.groupBy("segmentsAirlineName").count().filter(
    ~F.col("segmentsAirlineName").contains("||")  # Filter out combinations of multiple airlines
).orderBy("count", ascending=False)

# 1.4.2 Aircraft type distribution (based on frequency of segmentsEquipmentDescription)
# Removing duplicates in aircraft types
aircraft_type_distribution = df_cleaned.groupBy("segmentsEquipmentDescription").count().filter(
    ~F.col("segmentsEquipmentDescription").contains("||")  # Filter out combinations of aircraft types
).orderBy("count", ascending=False)

# Show the results
print("📌 Most Common Airlines:")
most_common_airlines.show(10, truncate=False)

print("📌 Aircraft Type Distribution:")
aircraft_type_distribution.show(10, truncate=False)