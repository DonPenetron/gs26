from typing import List, Dict

from utils import VLMModel
from utils import (
    parse_llm_list_dict_value
)


task_prompt = """
Carefully analyze the video for any instances of conflict, aggression, or hostile behavior. 
This includes physical fights, verbal harassment, intimidation, threats, or any other form of aggressive 
interaction between individuals.
Look for any physical fights, including but not limited to: hitting, 
kicking, punching, pushing, choking, grabbing, biting, or any other form of physical violence.
Scan for any behavior that could be interpreted as intimidation, bullying, stalking, or persistent harassment

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


class FightModel:
    def __init__(self, vlm_model: VLMModel):
        self.vlm_model = vlm_model

    def __call__(self, video_filepath: str) -> List[Dict[str, str]]:
        response = self.vlm_model.request(task_prompt, video_filepath)
        response_parsed = parse_llm_list_dict_value(response)
        return response_parsed