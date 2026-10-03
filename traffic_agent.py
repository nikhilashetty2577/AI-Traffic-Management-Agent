class TrafficManagementAgent:

    def __init__(self, traffic_data):
        self.traffic_data = traffic_data

    def calculate_priority_score(self, data):

        vehicle_score = min(
            data["vehicles"] / 100,
            1
        ) * 50

        waiting_score = min(
            data["waiting_time"] / 120,
            1
        ) * 40

        road_score = data["road_priority"] * 10

        return round(
            vehicle_score +
            waiting_score +
            road_score,
            2
        )

    def analyze_traffic(self):

        results = {}

        for direction, data in self.traffic_data.items():

            score = self.calculate_priority_score(data)

            results[direction] = {
                **data,
                "priority_score": score
            }

        return results

    def detect_emergency(self):

        return [
            direction
            for direction, data
            in self.traffic_data.items()
            if data["emergency"]
        ]

    def make_decision(self):

        results = self.analyze_traffic()

        emergency_directions = self.detect_emergency()

        # Give priority to emergency vehicles
        if emergency_directions:

            selected = max(
                emergency_directions,
                key=lambda direction:
                results[direction]["waiting_time"]
            )

            reason = (
                "Emergency vehicle detected. "
                "Emergency priority overrides "
                "normal traffic conditions."
            )

            return selected, reason, results

        # Select direction with highest score
        selected = max(
            results,
            key=lambda direction:
            results[direction]["priority_score"]
        )

        reason = (
            "The selected direction has the highest "
            "combined traffic priority score."
        )

        return selected, reason, results

    def calculate_green_time(self, direction):

        data = self.traffic_data[direction]

        # Emergency vehicle gets 45 seconds
        if data["emergency"]:
            return 45

        base_time = 15

        vehicle_bonus = min(
            int(data["vehicles"] * 0.3),
            25
        )

        waiting_bonus = min(
            int(data["waiting_time"] * 0.1),
            15
        )

        green_time = (
            base_time +
            vehicle_bonus +
            waiting_bonus
        )

        return min(
            green_time,
            60
        )

    def run_agent(self):

        selected, reason, results = self.make_decision()

        green_time = self.calculate_green_time(
            selected
        )

        return {
            "selected_direction": selected,
            "reason": reason,
            "green_time": green_time,
            "traffic_analysis": results,
            "emergency_detected":
                bool(self.detect_emergency())
        }