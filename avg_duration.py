%pyspark
from pyspark.sql import functions as F

# Define a function to convert 'travelDuration' (ISO 8601 format) to total minutes
def parse_duration(duration_str):
    hours = F.when(F.col("travelDuration").contains("H"), F.regexp_extract(F.col("travelDuration"), r"(\d+)H", 1).cast("double")).otherwise(0)
    minutes = F.when(F.col("travelDuration").contains("M"), F.regexp_extract(F.col("travelDuration"), r"(\d+)M", 1).cast("double")).otherwise(0)
    total_minutes = hours * 60 + minutes
    return total_minutes

# Filter out rows where 'travelDuration' and 'totalFare' are null or invalid
df_cleaned = df.filter(
    (F.col("travelDuration").isNotNull()) & 
    (F.col("travelDuration") != "") &
    (F.col("totalFare").isNotNull()) & 
    (F.col("totalFare") != 0.0)
)

# Add a new column 'travelDurationMinutes' for numerical representation
df_cleaned = df_cleaned.withColumn("travelDurationMinutes", parse_duration(F.col("travelDuration")))

# Group by both starting and destination airports and calculate average travel duration and price
df_cleaned.groupBy("startingAirport", "destinationAirport") \
    .agg(
        F.avg("travelDurationMinutes").alias("avg_duration"),  # Calculate average travel duration in minutes
        F.avg("totalFare").alias("avg_price")                   # Calculate average price
    ) \
    .orderBy("avg_duration") \
    .show(10)  # Show top 10 results