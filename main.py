Creating an eco-route-analyzer involves gathering data from APIs, processing that data, and calculating optimal routes based on the criteria of minimizing carbon emissions and fuel consumption. For demonstration purposes, the code provided below outlines how one might begin structuring such a program using Python, including making API requests, processing responses, and calculating optimal routes. Please note that some parts will require specific API keys and endpoints, which you will need to replace or implement based on the services you choose (e.g., Google Maps API, OpenWeatherMap, etc.).

```python
import requests
import json
import math
from datetime import datetime

# Constants and configurations
TRAFFIC_API_ENDPOINT = "your_traffic_api_endpoint_here"
WEATHER_API_ENDPOINT = "your_weather_api_endpoint_here"
API_KEY_TRAFFIC = "your_traffic_api_key"
API_KEY_WEATHER = "your_weather_api_key"

# Haversine formula to calculate distance between two points (latitude, longitude)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Fetch real-time traffic data for the route
def get_traffic_data(origin, destination):
    try:
        response = requests.get(f"{TRAFFIC_API_ENDPOINT}?origin={origin}&destination={destination}&key={API_KEY_TRAFFIC}")
        response.raise_for_status()  # Raise HTTPError for bad responses
        traffic_data = response.json()
        return traffic_data
    except requests.exceptions.RequestException as e:
        print("Error fetching traffic data:", e)
        return None

# Fetch weather data for a location
def get_weather_data(location):
    try:
        response = requests.get(f"{WEATHER_API_ENDPOINT}?q={location}&appid={API_KEY_WEATHER}")
        response.raise_for_status()  # Raise HTTPError for bad responses
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

# Calculate CO2 emissions based on distance, traffic, and weather
def calculate_co2_emissions(distance, traffic_conditions, weather_conditions):
    base_emission_factor = 0.21  # Average kg CO2 per km for a car
    traffic_factor = 1 + traffic_conditions.get("congestion_level", 0) * 0.1
    weather_factor = 1 + (weather_conditions.get("rain", 0) * 0.05 + weather_conditions.get("snow", 0) * 0.1)

    emissions = distance * base_emission_factor * traffic_factor * weather_factor
    return emissions

# Main function to calculate optimal route
def find_optimal_route(origins, destination):
    optimal_route = None
    minimal_emissions = float('inf')

    for origin in origins:
        print(f"Analyzing route from {origin} to {destination}.")
        distance = haversine(*origin.split(','), *destination.split(','))  # Calculate straight-line distance as a placeholder

        traffic_data = get_traffic_data(origin, destination)
        weather_data = get_weather_data(destination)

        if traffic_data is None or weather_data is None:
            print("Skipping route due to data fetch error.")
            continue

        traffic_conditions = {'congestion_level': traffic_data.get('congestion_level', 0)}
        weather_conditions = {'rain': weather_data.get('rain', 0), 'snow': weather_data.get('snow', 0)}

        emissions = calculate_co2_emissions(distance, traffic_conditions, weather_conditions)

        if emissions < minimal_emissions:
            minimal_emissions = emissions
            optimal_route = origin

    return optimal_route, minimal_emissions

# Main execution
if __name__ == '__main__':
    origins = ["40.7128,-74.0060", "34.0522,-118.2437"]  # Example coordinates (lat, lon)
    destination = "37.7749,-122.4194"  # Example destination (lat, lon)

    optimal_route, emissions = find_optimal_route(origins, destination)

    if optimal_route:
        print(f"The optimal route is from {optimal_route} with estimated emissions of {emissions:.2f} kg CO2.")
    else:
        print("Could not determine an optimal route.")
```

### Explanation:

1. **APIs and Keys**: You must replace the placeholder API endpoints and keys with actual values from your chosen traffic and weather data providers.

2. **Haversine Formula**: Used for calculating the great-circle distance between two points on the Earth; not accurate for actual driving distances but sufficient for this example.

3. **API Requests**: Requests are made to fetch both traffic and weather data. Error handling is included to manage network issues gracefully.

4. **CO2 Emissions Calculation**: A simple model that multiplies the base emissions with traffic and weather factors.

5. **Optimization Logic**: The program iterates over possible origins to find the one with minimal estimated emissions.

This program gives a foundational framework, but for a production version, one would need to extend functionality, implement better data processing, and refine calculations based on real-time API data.