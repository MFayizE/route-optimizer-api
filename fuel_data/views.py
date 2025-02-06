import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import load_fuel_data

ROUTING_API_KEY = settings.ROUTING_API_KEY
BASE_ROUTING_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

FUEL_EFFICIENCY = 10  
TANK_RANGE = 500  

class RouteOptimizerView(APIView):
    def get(self, request):
        start = request.GET.get("start")  
        finish = request.GET.get("finish") 

        if not start or not finish:
            return Response({"error": "Both start and finish locations are required."}, status=400)

        route_response = self.get_route(start, finish)
        if not route_response:
            return Response({"error": "Failed to retrieve route."}, status=500)

        route_distance = route_response["routes"][0]["summary"]["distance"] / 1609  
        fuel_stops, total_cost = self.calculate_fuel_stops(route_distance)

        return Response({
            "start": start,
            "finish": finish,
            "route_map": route_response["routes"][0]["geometry"],
            "total_distance_miles": round(route_distance, 2),
            "fuel_stops": fuel_stops,
            "total_fuel_cost": round(total_cost, 2),
        })

    def get_coordinates(self, location):

        geocode_url = f"https://api.openrouteservice.org/geocode/search?api_key={ROUTING_API_KEY}&text={location}"

        response = requests.get(geocode_url)
        if response.status_code == 200:
            data = response.json()
            if "features" in data and len(data["features"]) > 0:
                coordinates = data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
                return coordinates
        return None

    def get_route(self, start, finish):
        start_coords = self.get_coordinates(start)
        finish_coords = self.get_coordinates(finish)

        if not start_coords or not finish_coords:
            return {"error": "Failed to geocode start or finish location."}
        
        coordinates = [start_coords, finish_coords]  

        headers = {
            "Authorization": ROUTING_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "coordinates": coordinates,
            "profile": "driving-car",
            "format": "json"
        }


        response = requests.post(BASE_ROUTING_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            return {"error": f"Route API Error: {response_data.get('error', 'Unknown error')}"}

        if "routes" not in response_data:
            return {"error": "No route found. Please check your locations."}

        return response_data

    def calculate_fuel_stops(self, total_distance):

        stops_required = int(total_distance // TANK_RANGE)  
        fuel_stations = sorted(load_fuel_data(), key=lambda x: x["Retail Price"]) 
        fuel_stops = []
        total_cost = 0

        for _ in range(stops_required + 1):  
            if fuel_stations:
                best_station = fuel_stations.pop(0)  
                fuel_stops.append({
                    "name": best_station["Truckstop Name"],
                    "address": best_station["Address"],
                    "city": best_station["City"],
                    "state": best_station["State"],
                    "price_per_gallon": round(float(best_station["Retail Price"]), 2)
                })
                total_cost += float(best_station["Retail Price"]) * (TANK_RANGE / FUEL_EFFICIENCY)

        return fuel_stops, total_cost
