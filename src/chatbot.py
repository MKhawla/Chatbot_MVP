import json
from datetime import datetime
from typing import Dict, List, Optional

class TransportAPI:
    def __init__(self):
        # Simulated API data
        self.traffic_data = {
            "A1": {"congestion": "heavy", "speed": 30},
            "A2": {"congestion": "light", "speed": 90},
            "N1": {"congestion": "moderate", "speed": 50}
        }
        
        self.train_schedules = {
            "Paris-Lyon": [
                {"departure": "08:00", "arrival": "10:00", "available_seats": 45},
                {"departure": "10:00", "arrival": "12:00", "available_seats": 20},
            ],
            "Lyon-Paris": [
                {"departure": "09:00", "arrival": "11:00", "available_seats": 30},
                {"departure": "11:00", "arrival": "13:00", "available_seats": 50},
            ]
        }

    def get_traffic_status(self, road_id: str) -> Dict:
        return self.traffic_data.get(road_id, {"congestion": "unknown", "speed": 0})

    def get_train_schedule(self, route: str) -> List[Dict]:
        return self.train_schedules.get(route, [])

class RouteOptimizer:
    def __init__(self, transport_api: TransportAPI):
        self.api = transport_api
        
    def find_optimal_route(self, start: str, end: str, preferred_mode: str) -> Dict:
        if preferred_mode == "car":
            # Simplified routing logic
            routes = {
                ("Paris", "Lyon"): ["A1", "A2"],
                ("Lyon", "Paris"): ["A2", "A1"]
            }
            
            route_roads = routes.get((start, end), [])
            if not route_roads:
                return {"status": "error", "message": "No route found"}
            
            # Check traffic on each road
            total_time = 0
            congestion_status = []
            for road in route_roads:
                traffic = self.api.get_traffic_status(road)
                total_time += 100 / traffic["speed"]  # Simplified time calculation
                congestion_status.append(f"{road}: {traffic['congestion']}")
            
            return {
                "status": "success",
                "mode": "car",
                "estimated_time": round(total_time, 1),
                "traffic_info": congestion_status
            }
            
        elif preferred_mode == "train":
            route_key = f"{start}-{end}"
            schedules = self.api.get_train_schedule(route_key)
            if not schedules:
                return {"status": "error", "message": "No trains found"}
            
            # Find next available train
            current_time = datetime.now().strftime("%H:%M")
            for schedule in schedules:
                if schedule["departure"] > current_time and schedule["available_seats"] > 0:
                    return {
                        "status": "success",
                        "mode": "train",
                        "departure": schedule["departure"],
                        "arrival": schedule["arrival"],
                        "available_seats": schedule["available_seats"]
                    }
            
            return {"status": "error", "message": "No available trains"}
        
        return {"status": "error", "message": "Unsupported transport mode"}

class TravelChatbot:
    def __init__(self):
        self.transport_api = TransportAPI()
        self.route_optimizer = RouteOptimizer(self.transport_api)
        
    def process_query(self, query: str) -> str:
        # Simple keyword-based query processing
        query = query.lower()
        
        if "route" in query or "travel" in query:
            # Extract cities from query (simplified)
            if "paris" in query and "lyon" in query:
                start = "Paris"
                end = "Lyon"
                
                # Check both car and train options
                car_route = self.route_optimizer.find_optimal_route(start, end, "car")
                train_route = self.route_optimizer.find_optimal_route(start, end, "train")
                
                response = f"Here are your travel options from {start} to {end}:\n\n"
                
                if car_route["status"] == "success":
                    response += "By Car:\n"
                    response += f"Estimated time: {car_route['estimated_time']} hours\n"
                    response += "Traffic conditions:\n"
                    for info in car_route['traffic_info']:
                        response += f"- {info}\n"
                    response += "\n"
                
                if train_route["status"] == "success":
                    response += "By Train:\n"
                    response += f"Next available train:\n"
                    response += f"- Departure: {train_route['departure']}\n"
                    response += f"- Arrival: {train_route['arrival']}\n"
                    response += f"- Available seats: {train_route['available_seats']}\n"
                
                return response
            
        return "I'm sorry, I couldn't understand your query. Please ask about routes between supported cities (e.g., Paris and Lyon)."

def main():
    chatbot = TravelChatbot()
    
    print("Welcome to the Travel Assistant! (Type 'quit' to exit)")
    print("You can ask about routes between Paris and Lyon")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.process_query(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()