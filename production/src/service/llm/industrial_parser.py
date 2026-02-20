from typing import List, Dict

from utils import VLMModel
from utils import (
    parse_llm_list_dict_value
)


task_prompt = """
Analyze the video frame by frame to identify all production incidents. Look for and list each incident 
with timestamp (if available) and a brief description. Focus on the following categories:  
- **Safety violations** (e.g., improper PPE, unauthorized access, unsafe behavior)  
- **Falling cargo or materials** (e.g., objects dropping from conveyor, racks, or overhead)  
- **Equipment jamming or malfunction** (e.g., conveyor belt jam, machine stalling)  
- **Structural collapse or instability** (e.g., rack collapse, conveyor failure, support failure)  
- **Dangerous zones** (e.g., moving machinery, pinch points, unguarded areas, workers in hazardous zones)  
- **Near misses or potential hazards** (e.g., almost falling object, worker narrowly avoiding machinery)  
- **Other production disruptions** (e.g., spillage, fire, smoke, electrical hazards)  

For each accident you detect, provide:
1. TIMESTAMP: The exact second when the accident occurs
2. DESCRIPTION: Brief description of what happens

In the response, return the following json list:
[
    {
        "timestamp": "TIMESTAMP_i",
        "description": "DESCRIPTION_i",
    }
], where 
"TIMESTAMP_i" - the second at which the ith event started, embed seconds in " symbol;
"DESCRIPTION_i" - is the description of the ith event, in a few sentences.

Answer constraints:
- Return only json list. Don't add your comments.
- If there are no accidents on video return empty list.
- Mention in list all suspicious cases.
- Mention only things that really occur on video. Don't invent anything on your own.
"""


class IndustrialModel:
    def __init__(self, vlm_model: VLMModel):
        self.vlm_model = vlm_model

    def __call__(self, video_filepath: str) -> List[Dict[str, str]]:
        response = self.vlm_model.request(task_prompt, video_filepath)
        response_parsed = parse_llm_list_dict_value(response)
        return response_parsed