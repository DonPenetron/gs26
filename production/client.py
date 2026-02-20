import logging
from fastapi import FastAPI
from pydantic import BaseModel

from worker import parse_document_task, parse_document_custom_task

class RequestModel(BaseModel):
    task_id: str
    video_filename: str

class RequestModelCustom(BaseModel):
    task_id: str
    video_filename: str
    prompt: str

app = FastAPI()


@app.post("/ml/parse_video")
def parse_video(request: RequestModel):
    parse_document_task.delay(request.task_id, request.video_filename)


@app.post("/ml/parse_video_custom")
def parse_video_custom(request: RequestModelCustom):
    parse_document_custom_task.delay(request.task_id, request.video_filename, request.prompt)