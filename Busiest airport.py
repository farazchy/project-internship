%pyspark
from pyspark.sql import functions as F

# Top 10 busiest airports (based on frequency in startingAirport)
busiest_airports_starting = df.groupBy("startingAirport").count().orderBy("count", ascending=False).limit(10)

# Top 10 busiest airports (based on frequency in destinationAirport)
busiest_airports_destination = df.groupBy("destinationAirport").count().orderBy("count", ascending=False).limit(10)

# Show the results for starting airports
print("📌 Top 10 Busiest Departures Airports:")
busiest_airports_starting.show()

# Show the results for destination airports
print("📌 Top 10 Busiest Arrivals Airports:")
busiest_airports_destination.show()
