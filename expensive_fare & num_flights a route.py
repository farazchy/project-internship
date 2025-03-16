%pyspark
from pyspark.sql import functions as F

# Clean data: Convert necessary columns to proper types and handle null values
df_cleaned = df.withColumn(
    "isbasiceconomy", F.coalesce((F.col("isbasiceconomy") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isrefundable", F.coalesce((F.col("isrefundable") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isnonstop", F.coalesce((F.col("isnonstop") == "TRUE").cast("boolean"), F.lit(False))
)

# Drop rows where any of the critical columns (basefare, totalFare, or seatsremaining) are equal to 0.0
df_cleaned = df_cleaned.filter(
    (F.col("basefare") != 0.0) & 
    (F.col("totalFare") != 0.0) & 
    (F.col("seatsremaining") != 0)
)

# Drop rows with any null values in the DataFrame
df_cleaned = df_cleaned.dropna()

# Fill null values in numeric columns with default values (zero for most numeric fields)
df_cleaned = df_cleaned.fillna({
    "basefare": 0.0,
    "totalFare": 0.0,
    "seatsremaining": 0,
    "totaltraveldistance": 0,
    "elapseddays": 0
})

# Fill other columns with specific rules, like filling nulls with empty strings or zero for unknown data
df_cleaned = df_cleaned.fillna({
    "segmentsdeparturetimeepochseconds": 0,  # Assuming a default value for time columns
    "segmentsarrivalairportcode": "Unknown",  # Fill unknown airports
    "segmentsdepartureairportcode": "Unknown",
    "segmentsairlinename": "Unknown",
    "segmentsairlinecode": "Unknown",
    "segmentsequipmentdescription": "Unknown"
})

# Group by destinationAirport and startingAirport to calculate cheapest and most expensive fares
cheapest_and_expensive_flights = df_cleaned.groupBy("destinationairport", "startingairport") \
    .agg(
        F.min("totalFare").alias("cheapest_fare"),
        F.max("totalFare").alias("most_expensive_fare"),
        F.count("totalFare").alias("num_flights")  # Count the number of flights for each route
    ) \
    .filter(F.col("num_flights") > 1)  # Filter out routes with only 1 flight (where cheapest and most expensive fares are the same)

# Order the results by the cheapest fare
cheapest_and_expensive_flights = cheapest_and_expensive_flights.orderBy("cheapest_fare")

# Show the results with destination airport, starting airport, cheapest fare, and most expensive fare
cheapest_and_expensive_flights.show(10, truncate=False)