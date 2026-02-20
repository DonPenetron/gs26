from typing import List, Dict

from utils import VLMModel
from utils import (
    parse_llm_list_dict_value
)


task_prompt = """
Analyze this video carefully and identify all traffic accidents and dangerous behaviour cases.
A traffic accident and dageroues behaviour is defined as any abnormal behavior on the road. 
A detailed description of such cases is provided below:

* Sudden stops or slowdowns in traffic
* Vehicles swerving or changing lanes abruptly
* Cars that appear to be in distress or have their lights on
* Vehicles that are stationary for an extended period
* Cars that are moving at unusual speeds


For each accident you detect, provide:
1. TIMESTAMP: The exact second when the accident occurs
2. DESCRIPTION: Brief description of what happens
3. SEVERITY: Minor/Moderate/Severe

In the response, return the following json list:
[
    {
        "timestamp": "TIMESTAMP_i",
        "description": "DESCRIPTION_i",
        "severity": "SEVERITY_i",
    }
], where 
"TIMESTAMP_i" - the second at which the ith event started, embed seconds in " symbol;
"DESCRIPTION_i" - is the description of the ith event, in a few sentences;
"SEVERITY_i" - is the severity of the outcome of the ith event.

Answer constraints:
- Return only json list. Don't add your comments.
- If there are no accidents on video return empty list.
- Mention in list all suspicious cases.
- Mention only things that really occur on video. Don't invent anything on your own.
"""


class TrafficModel:
    def __init__(self, vlm_model: VLMModel):
        self.vlm_model = vlm_model

    def __call__(self, video_filepath: str) -> List[Dict[str, str]]:
        response = self.vlm_model.request(task_prompt, video_filepath)
        response_parsed = parse_llm_list_dict_value(response)
        return response_parsed