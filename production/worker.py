import os
import logging
import requests
from celery import Celery
from minio import Minio
import uuid

from utils import VLMModel, VideoManager, Highlighter
from service import MasterModel

# import torch
# logging.warning(torch.cuda.is_available())

VLM_URL = os.environ.get("VLM_URL")
REDIS_BROKER_URL = os.environ.get("REDIS_BROKER_URL")
REDIS_BACKEND_URL = os.environ.get("REDIS_BACKEND_URL")
BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
BACKEND_URL_PAYLOAD = "http://45.80.129.41:8001/api/highlights/bulk/"
BACKEND_URL_FINAL = "http://45.80.129.41:8001/api/logistic/tasks"


app = Celery(
    "analyzer",
    broker=REDIS_BROKER_URL, 
    backend=REDIS_BACKEND_URL
)
vlm_model = VLMModel(VLM_URL)
parser = MasterModel(vlm_model)
minio_client = Minio(
    "45.80.129.41:9000",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def make_name(idx: int):
    if 0 <= idx < 10:
        return f"00{idx}"
    elif 10 <= idx < 100:
        return f"0{idx}"
    return str(idx)

@app.task
def parse_document_task(task_id: str, video_filename: str):
    minio_client.fget_object(BUCKET_NAME, video_filename, "./video.mp4")
    video_manager = VideoManager("./video.mp4", "/video")
    chunks_meta, split_destination = video_manager.split()
    hightlighter = Highlighter("./video.mp4", "/video")
    segments = list()
    for item in chunks_meta:
        cur_result = parser.parse_video(
            os.path.join(split_destination, f"chunk_{make_name(item['chunk_idx'])}.mp4")
        )
        cur_result_n = list()
        for r in cur_result:
            r_n = {**r}
            r_n["task_id"] = task_id
            r_n["time_start"] = str(float(r_n["time_start"]) + float(item["time_start"]))
            cur_result_n.append(r_n)
        segments.extend(cur_result_n)

        response = requests.post(
            BACKEND_URL_PAYLOAD,
            json=cur_result_n,
            headers={"Content-Type": "application/json"},
        )
        logging.warning(response.content)
    response = requests.patch(
        f"{BACKEND_URL_FINAL}/{task_id}/status/",
        json={"status": "success"}
    )
    logging.warning(response.content)
    hightlighter.get_highlights(segments)
    filename = str(uuid.uuid4())
    objects = list()
    for item in os.listdir(hightlighter.get_folder()):
        minio_client.fput_object(
            BUCKET_NAME,
            f"{filename}_{item}",
            os.path.join(hightlighter.get_folder(), item)
        )
        objects.append(f"{filename}_{item}")
    requests.post("http://45.80.129.41:8001/api/highlight-files/upload/", json={"task_id": task_id, "paths": objects})


@app.task
def parse_document_custom_task(task_id: str, video_filename: str, description: str):
    minio_client.fget_object(BUCKET_NAME, video_filename, "./video.mp4")
    video_manager = VideoManager("./video.mp4", "/video")
    chunks_meta, split_destination = video_manager.split()
    for item in chunks_meta:
        cur_result = parser.parse_video_custom(
            os.path.join(split_destination, f"chunk_{make_name(item['chunk_idx'])}.mp4"),
            description
        )
        cur_result_n = list()
        for r in cur_result:
            r_n = {**r}
            r_n["task_id"] = task_id
            r_n["time_start"] = str(float(r_n["time_start"]) + float(item["time_start"]))
            cur_result_n.append(r_n)

        logging.warning("ITEMS")
        logging.warning(cur_result_n)
        response = requests.post(
            BACKEND_URL_PAYLOAD,
            json=cur_result_n,
            headers={"Content-Type": "application/json"},
        )
        logging.warning("RESPONSE")
        logging.warning(response.content)
    response = requests.patch(
        f"{BACKEND_URL_FINAL}/{task_id}/status/",
        json={"status": "success"}
    )
    logging.warning(response.content)