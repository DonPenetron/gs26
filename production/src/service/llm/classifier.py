import logging
from utils import VLMModel


CLASSES = {
    "1": "TRAFFIC",
    "2": "INDUSTRIAL",
    "3": "FIGHT",
    "4": "EMPTY",
}


task_prompt = """
You are a high-reliability video analysis assistant. Your task is to analyze the provided video frame-by-frame and 
classify it into exactly one of the following four categories. Use the detailed definitions and visual cues provided. 

Categories:
1. Car accident.
Visual cues:
"Vehicle collision or impact",
"Sudden, violent deceleration of vehicles",
"Deformation of car bodies (dents, crushed bumpers)",
"Airbag deployment",
"Glass shattering or debris on roadway",
"Vehicles leaving the roadway or flipping",
"Emergency services (police, ambulance) present",
"Pedestrians reacting in alarm near vehicles"

Exclude if: This is a staged event, a video game, or a simulation without real-world consequences

2. Production incident.
Visual cues:
"Industrial machinery malfunction (jamming, unexpected stops)",
"Sparks, smoke, or fire from equipment",
"Object falling from conveyor belt or height",
"Worker in distress near machinery (e.g., hand caught, sudden recoil)",
"Fluid leak (hydraulic, chemical) from pipes or machines",
"Structural failure of equipment (shelving collapsing, arm breaking)",
"Robotic arm moving erratically or colliding"

Exclude if: "The environment is not industrial/manufacturing, or the event is part of normal, safe operation (e.g., planned maintenance)."

3. Fight aggression
Visual cues:
"Physical striking (punching, kicking, slapping)",
"Pushing, shoving, or grappling between individuals",
"Objects being thrown or used as weapons",
"Aggressive postures (chest-puffing, finger-pointing in face)",
"Sudden, rapid movements indicating a chase or flight from aggression",
"Group forming around two individuals in conflict",
"Individual falling to the ground due to force from another"

Exclude if: "The interaction is clearly sport-related (boxing match, martial arts) or playful (rough-housing without intent to harm)."

4. None of the above

In response return one digit (1-4) - number of a class.
"""


class ClassifierModel:
    def __init__(self, vlm_model: VLMModel):
        self.vlm_model = vlm_model
        self.class_encoding = CLASSES

    def __call__(self, video_filepath: str):
        response = self.vlm_model.request(task_prompt, video_filepath)
        response = self.class_encoding.get(response[0])
        if response is None:
            return "EMPTY"
        return response