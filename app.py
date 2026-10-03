from flask import Flask, render_template, request, jsonify

from traffic_agent import TrafficManagementAgent
from route_planner import RoutePlanner
from llm_agent import TrafficIntelligenceAgent

import os


app = Flask(__name__)

route_planner = RoutePlanner()
llm_agent = TrafficIntelligenceAgent()

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Traffic analysis
@app.route("/api/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    traffic_data = {

        "North": {
            "vehicles": int(data["north_vehicles"]),
            "waiting_time": int(data["north_wait"]),
            "road_priority": 1,
            "emergency": data["emergency"] == "North"
        },

        "South": {
            "vehicles": int(data["south_vehicles"]),
            "waiting_time": int(data["south_wait"]),
            "road_priority": 1,
            "emergency": data["emergency"] == "South"
        },

        "East": {
            "vehicles": int(data["east_vehicles"]),
            "waiting_time": int(data["east_wait"]),
            "road_priority": 1,
            "emergency": data["emergency"] == "East"
        },

        "West": {
            "vehicles": int(data["west_vehicles"]),
            "waiting_time": int(data["west_wait"]),
            "road_priority": 1,
            "emergency": data["emergency"] == "West"
        }
    }

    # Create the AI traffic agent
    agent = TrafficManagementAgent(
        traffic_data
    )

    # Run the agent
    result = agent.run_agent()

    return jsonify(result)
# LLM Traffic Explanation
@app.route("/api/explain", methods=["POST"])
def explain():

    data = request.get_json()

    explanation = llm_agent.explain_decision(
        selected_direction=data["selected_direction"],
        green_time=data["green_time"],
        traffic_analysis=data["traffic_analysis"],
        emergency_detected=data["emergency_detected"]
    )

    return jsonify({
        "success": True,
        "explanation": explanation
    })


# A* route planning
@app.route("/api/route", methods=["POST"])
def route():

    data = request.get_json()

    start = data.get("start")
    destination = data.get("destination")

    route, cost = route_planner.find_route(
        start,
        destination
    )

    if route is None:

        return jsonify({
            "success": False,
            "message": "No route found."
        })

    return jsonify({
        "success": True,
        "route": route,
        "cost": cost
    })


# Start Flask server
if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )