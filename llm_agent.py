import os
from google import genai


class TrafficIntelligenceAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Primary and fallback models
        self.models = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite"
        ]

    def explain_decision(
        self,
        selected_direction,
        green_time,
        traffic_analysis,
        emergency_detected
    ):

        traffic_summary = ""

        for direction, data in traffic_analysis.items():

            traffic_summary += (
                f"{direction}: "
                f"{data['vehicles']} vehicles, "
                f"{data['waiting_time']} seconds waiting, "
                f"priority score "
                f"{data['priority_score']}. "
            )

        if emergency_detected:

            situation = (
                "An emergency vehicle has been detected. "
                "Emergency priority must be explained first."
            )

        else:

            situation = (
                "No emergency vehicle is detected. "
                "The decision is based on traffic conditions."
            )

        prompt = f"""
You are the Traffic Intelligence Agent
inside an AI-based traffic management system.

Analyze the traffic decision made by the system.

Selected direction:
{selected_direction}

Green signal duration:
{green_time} seconds

Traffic conditions:
{traffic_summary}

Emergency status:
{emergency_detected}

Situation:
{situation}

Give a short explanation in simple student-friendly language.

Your explanation must contain:
1. Why this direction was selected.
2. How vehicle count and waiting time affected the decision.
3. Whether emergency priority was involved.
4. Why the green signal duration is appropriate.

Do not change the selected direction.
Do not invent traffic data.
"""

        last_error = None

        # Try each model
        for model in self.models:

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return response.text

            except Exception as error:

                last_error = error

                print(
                    f"Gemini model {model} failed:"
                )
                print(error)

        # If all models fail
        return (
            "The AI traffic decision was completed successfully, "
            "but the Gemini explanation service is temporarily "
            "unavailable. Please try again."
        )