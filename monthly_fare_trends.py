%pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Clean dataset as before
df_cleaned = df.withColumn(
    "isbasiceconomy", F.coalesce((F.col("isbasiceconomy") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isrefundable", F.coalesce((F.col("isrefundable") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isnonstop", F.coalesce((F.col("isnonstop") == "TRUE").cast("boolean"), F.lit(False))
)

# Filter and clean the data
df_cleaned = df_cleaned.filter(
    (F.col("basefare") != 0.0) & 
    (F.col("totalFare") != 0.0) & 
    (F.col("seatsremaining") != 0)
)

df_cleaned = df_cleaned.dropna()

# Add a new column for "week" or "month" (we're using month as an example)
df_cleaned = df_cleaned.withColumn("searchMonth", F.month(F.col("searchDate")))

# Group by the month and calculate the average price trends per month
price_trends = df_cleaned.groupBy("searchMonth", "startingairport", "destinationairport") \
    .agg(F.avg("totalFare").alias("avg_fare"), 
         F.min("totalFare").alias("min_fare"),
         F.max("totalFare").alias("max_fare"),
         F.stddev("totalFare").alias("stddev_fare")) \
    .orderBy("searchMonth")

# Show the result
price_trends.show(10)
