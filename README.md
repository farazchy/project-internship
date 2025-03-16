Project Overview
The Ticket Meta Search & Recommendation project integrates multiple datasets from airlines, airports, and online travel agencies to provide users with personalized and efficient flight search capabilities. Utilizing big data and AI, the system provides recommendations on when and where to fly, predicts the best times to purchase tickets, and optimizes flight routes for cost-efficiency.

Key functionalities include:
Dynamic Flight Search: Search for available flights based on user preferences such as departure location, destination, travel dates, and budget.

AI-Powered Chatbot: A chatbot that assists users in flight booking by analyzing historical flight data and providing personalized recommendations.

Flight Route Optimization: Optimizes flight routes by considering alternative routes, multi-stop options, and minimizing layover times and costs.

Data Visualization: Visualizes data trends and patterns, such as price fluctuations over time, seasonal trends, and price comparisons across different airlines.


Features:

Flight Search & Booking
Search for flights based on airport codes.
View detailed information like price, duration, and airline.

AI-Powered Chatbot
Receive personalized flight recommendations.
Interactive real-time responses based on the dataset and AI.

Dynamic Flight Route Map
Visualize flight routes on an interactive map.
Supports various visual features, such as Bézier curves for high-traffic routes.

Price Trend Insights
Display historical price trends for selected routes.
Helps users make informed decisions on when to book their tickets.

Real-Time Flight Data
Provides up-to-date flight availability and pricing.

Where to Fly & When to Fly
Suggest destinations based on the lowest prices and travel time.
Provides the best times to fly, ensuring cost-effective travel plans.


Technologies Used:

Big Data Technologies:
Hadoop: For distributed storage and processing of large flight-related datasets.
Apache Spark: For big data processing and analytics.
Hive: For data warehousing and querying.

AI & Machine Learning:
ChatGPT API: For AI-powered recommendations based on historical and real-time data.
Predictive Analytics: For forecasting ticket prices and optimizing routes.

Data Visualization:
Leaflet.js: For building interactive flight route maps.
Chart.js: For displaying price trends over time.

Backend:
Node.js/Express: For the server-side API.
MySQL: For storing flight, airline, and pricing data.

Frontend:
JavaScript: For building the interactive and dynamic user interface.
HTML/CSS: For website layout and design, including dark mode support.


Data Analysis & Visualization:

The project leverages dimensional modeling to create a data warehouse containing supplementary dimension data such as:

Airport information (name, code, location).
City data (city name, code, latitude/longitude).
Airline information (country, alliance).
Aircraft model and manufacturer details.

Visualization Analysis
Perform analysis across multiple dimensions such as price, duration, and location.
Visualize key data points on interactive maps, helping users make informed decisions.
Display dynamic price trend charts to show historical price fluctuations.

AI-Powered Recommendations
The project utilizes ChatGPT to offer personalized flight recommendations and insights based on user input. By analyzing historical and real-time data, the chatbot provides:

Price Predictions: When the best time to book tickets is based on seasonal trends and demand.
Optimized Routes: Suggests cost-effective flight routes and multi-stop combinations.
Dynamic Recommendations: Based on user preferences, the chatbot can dynamically recommend the best flight options.

Route Optimization
The flight route optimization system is built on a graph-based model where airports are nodes and flight connections are weighted edges. The model optimizes routes by considering:

Cost: Finding cheaper alternatives to direct flights.
Layover Time: Minimizing layover durations for a more efficient journey.
Travel Duration: Optimizing overall travel time by suggesting the quickest routes.
Airline Alliances: Considering airline partnerships to reduce costs and provide more seamless travel experiences.


Website & Chatbot:

The website serves as the main user interface for the project. It allows users to interact with various features such as searching for flights, viewing flight prices, and getting personalized recommendations.

Website Features:
Search Interface: Allows users to search for flights by specifying departure and destination airports, travel dates, and preferences.
Flight Results: Displays available flights with detailed information, including price, duration, and airline.
Flight Route Map: An interactive map to visualize flight routes and travel paths.
Price Trend Insights: Graphs that show historical price trends to help users make informed decisions about when to book flights.

AI-Powered Chatbot:
The ChatGPT-powered chatbot is integrated into the website to provide users with personalized flight recommendations.
It can suggest the best times to fly based on historical pricing trends and assist users in finding the most cost-effective routes.
The chatbot can dynamically update based on user input, offering real-time flight options and information.
