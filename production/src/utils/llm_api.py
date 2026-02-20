import requests


class VLMModel:
    def __init__(self, vlm_url: str):
        self.vlm_url = vlm_url

    def request(self, task_prompt: str, video_path: str, max_tokens: int = 1024, temperature: int = 0):
        video_url = f"file://{video_path}"
        data = {
            "messages": [
                {"role": "user", "content": [
                    {
                        "type": "text", 
                        "text": task_prompt
                    },
                    {
                        "type": "video_url",
                        "video_url": {"url": video_url}
                    },
                ]}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(self.vlm_url, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"status_code: {response.status_code}"