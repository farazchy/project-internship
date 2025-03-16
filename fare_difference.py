%pyspark
from pyspark.sql import functions as F

# Ensure clean data with only valid fares
df_cleaned = df.filter(
    (F.col("totalFare").isNotNull()) & 
    (F.col("startingAirport").isNotNull()) & 
    (F.col("destinationAirport").isNotNull()) &
    (F.col("totalFare") > 0)  # Remove invalid fares
)

# Find cheapest non-stop fares
nonstop_fares = df_cleaned.filter(df_cleaned['isNonStop'] == True) \
    .groupBy("startingAirport", "destinationAirport") \
    .agg(F.min("totalFare").alias("cheapest_nonstop_fare"))

# Find cheapest layover fares (only 1 layover, exclude multi-stop flights)
layover_fares = df_cleaned.filter(df_cleaned['isNonStop'] == False) \
    .withColumn("layover_count", F.size(F.split(F.col("segmentsDepartureAirportCode"), "\|\|"))) \
    .filter(F.col("layover_count") == 2) \
    .groupBy("startingAirport", "destinationAirport") \
    .agg(F.min("totalFare").alias("cheapest_layover_fare"))

# Join both datasets to compare fares
price_comparison = nonstop_fares.join(
    layover_fares,
    on=["startingAirport", "destinationAirport"],
    how="outer"
)

# Ensure Unavailable is assigned properly
price_comparison = price_comparison.withColumn(
    "cheapest_nonstop_fare",
    F.when(F.col("cheapest_nonstop_fare").isNull(), "Unavailable").otherwise(F.col("cheapest_nonstop_fare"))
)

price_comparison = price_comparison.withColumn(
    "cheapest_layover_fare",
    F.when(F.col("cheapest_layover_fare").isNull(), "Unavailable").otherwise(F.col("cheapest_layover_fare"))
)

# Correct fare difference calculation
price_comparison = price_comparison.withColumn(
    "fare_difference",
    F.when(
        (F.col("cheapest_layover_fare") == "Unavailable") | (F.col("cheapest_nonstop_fare") == "Unavailable"),
        "Unavailable"
    ).otherwise(F.round(F.col("cheapest_nonstop_fare") - F.col("cheapest_layover_fare"), 2))
)

# Remove cases where layover fare is greater than non-stop fare (since layovers should be cheaper)
price_comparison = price_comparison.filter(
    (F.col("fare_difference") == "Unavailable") | (F.col("fare_difference") >= 0)
)

# Show the final result
price_comparison.show(10)  # Show top 10 results