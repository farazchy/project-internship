%pyspark
from pyspark.sql import functions as F
import random

# Assuming df is already loaded and cleaned

# Clean dataset
df_cleaned = df.withColumn(
    "isbasiceconomy", F.coalesce((F.col("isbasiceconomy") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isrefundable", F.coalesce((F.col("isrefundable") == "TRUE").cast("boolean"), F.lit(False))
).withColumn(
    "isnonstop", F.coalesce((F.col("isnonstop") == "TRUE").cast("boolean"), F.lit(False))
)

# Filter out rows where any of the critical columns (basefare, totalFare, or seatsremaining) are equal to 0.0
df_cleaned = df_cleaned.filter(
    (F.col("basefare") != 0.0) & 
    (F.col("totalFare") != 0.0) & 
    (F.col("seatsremaining") != 0)
)

# Drop rows with any null values in the DataFrame
df_cleaned = df_cleaned.dropna()

# 1. Daily Price Variation Trends (Multiple Dates)
# Get the list of unique flight dates
unique_flight_dates = df_cleaned.select("flightDate").distinct().rdd.flatMap(lambda x: x).collect()

# If there are at least 5 dates, randomly sample 5; otherwise, use all available dates
num_dates_to_sample = min(10, len(unique_flight_dates))  # Here we are sampling up to 10 flight dates

# Sample the dates if there are at least one
random_dates = random.sample(unique_flight_dates, num_dates_to_sample)

# Filter the dataframe for those random dates
daily_price_trends = df_cleaned.filter(F.col("flightDate").isin(random_dates)) \
    .groupBy("flightDate") \
    .agg(F.avg("totalFare").alias("avg_fare"), 
         F.min("totalFare").alias("min_fare"),
         F.max("totalFare").alias("max_fare")) \
    .orderBy("flightDate")

# Show Results
print("📌 Daily Price Variation Trends:")
daily_price_trends.show(10, truncate=False)

# 2. Weekday vs Weekend Fare Differences
# Add a new column indicating whether the day is a weekend or weekday
df_cleaned = df_cleaned.withColumn("day_of_week", F.date_format("flightDate", "u").cast("int"))
df_cleaned = df_cleaned.withColumn("is_weekend", F.when((F.col("day_of_week") == 6) | (F.col("day_of_week") == 7), 1).otherwise(0))

# Calculate the average fare for weekdays vs weekends
weekend_vs_weekday_fare = df_cleaned.groupBy("is_weekend") \
    .agg(F.avg("totalFare").alias("avg_fare"))

# Show Results
print("📌 Weekday vs Weekend Fare Differences:")
weekend_vs_weekday_fare.show(2, truncate=False)

# 3. Seasonal Price Trends (Holiday vs Non-Holiday)
# Extract month and holiday periods
df_cleaned = df_cleaned.withColumn("month", F.month(F.col("flightDate")))

# Identify holiday months or special pricing periods, such as December (holiday season)
df_cleaned = df_cleaned.withColumn("is_holiday_season", F.when(F.col("month").isin([12, 1]), 1).otherwise(0))

# Group by month to observe seasonal pricing trends for both holiday and non-holiday
seasonal_trends = df_cleaned.groupBy("month", "is_holiday_season") \
    .agg(F.avg("totalFare").alias("avg_fare")) \
    .orderBy("month")

# Show Results
print("📌 Seasonal Price Trends (Holiday vs Non-Holiday):")
seasonal_trends.show(12, truncate=False)

# 4. Booking Lead Time (How many days in advance to book for best fares)
# Calculate the days between booking (searchDate) and the flight (flightDate)
df_cleaned = df_cleaned.withColumn("days_to_flight", F.datediff(F.col("flightDate"), F.col("searchDate")))

# Group by the lead time (days_to_flight) to analyze booking patterns
booking_lead_time = df_cleaned.groupBy("days_to_flight") \
    .agg(F.avg("totalFare").alias("avg_fare")) \
    .orderBy("days_to_flight")

# Show Results
print("📌 Booking Lead Time Analysis:")
booking_lead_time.show(10, truncate=False)
