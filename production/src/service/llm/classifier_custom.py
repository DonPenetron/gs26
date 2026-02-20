import re
from utils import VLMModel


task_prompt = """
You will be given a video. You will also be provided with a detailed description of some event/situation. 
Your task is to carefully analyze the video and tell if this video contains the event presented in the description. 
If yes, then return the number "1" in the answer, otherwise "0". Don't add your comments in the reply.

=== Description of event ===
DESCRIPTION
"""


class ClassifierModelCustom:
    def __init__(self, vlm_model: VLMModel):
        self.vlm_model = vlm_model

    def __call__(self, video_filepath: str, description: str):
        task_prompt_cur = re.sub("DESCRIPTION", description, task_prompt)
        response = self.vlm_model.request(task_prompt_cur, video_filepath)
        return response[0] == "1"