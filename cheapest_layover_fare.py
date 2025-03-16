%pyspark
from pyspark.sql import functions as F

# Filter for layover flights and calculate the cheapest layover fare for each departure and arrival airport combination
layover_fares = df.filter(df["isNonStop"] == False) \
    .groupBy("segmentsDepartureAirportCode", "segmentsArrivalAirportCode") \
    .agg(F.min("totalFare").alias("cheapest_layover_fare")) \
    .orderBy("cheapest_layover_fare")  # Order by cheapest layover fare

# Show the top 10 layovers with the cheapest fare
layover_fares.show(10)