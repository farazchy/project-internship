%pyspark
from pyspark.sql import functions as F

# Group by both startingAirport and destinationAirport and calculate the average seatsRemaining for each pair
seat_availability = df.groupBy("startingAirport", "destinationAirport") \
    .agg(F.avg("seatsRemaining").alias("avg_seats_left")) \
    .orderBy("avg_seats_left", ascending=False) \
    .show(10)  # Show top 10 results