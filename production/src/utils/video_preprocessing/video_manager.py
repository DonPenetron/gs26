import os
import shutil
import logging
import subprocess


class VideoManager:
    def __init__(self, source_path: str, destination_path: str):
        self.source_path = source_path
        self.destination_path = destination_path
        self.video_duration = None
        self.video_split_folder = "video_split"
        self._prepare()

    def _prepare(self):
        assert os.path.isdir(self.destination_path)
        if os.path.exists(os.path.join(self.destination_path, self.video_split_folder)):
            shutil.rmtree(os.path.join(self.destination_path, self.video_split_folder))
        os.mkdir(os.path.join(self.destination_path, self.video_split_folder))
        self.video_duration = self.get_duration(self.source_path)

    def split(self, chunk_duration: int = 60, stride_duration: int = 50):
        os.system(
            ("ffmpeg "
             + f" -i {self.source_path} " 
             + " -c copy "
             + " -f segment "
             + " -reset_timestamps 1 "
             + f" -segment_time {chunk_duration} "
             + os.path.join(self.destination_path, self.video_split_folder, "chunk_%03d.mp4"))
        )
        
        chunk_filenames = os.listdir(os.path.join(self.destination_path, self.video_split_folder))
        chunk_filenames = sorted(chunk_filenames, key=lambda x: int(os.path.splitext(x)[0].split("_")[1]))
        chunks_meta = list()
        for item in chunk_filenames:
            idx = int(os.path.splitext(item)[0].split("_")[1])
            filepath = os.path.join(self.destination_path, self.video_split_folder, item)
            duration = self.get_duration(filepath)
            logging.warning(duration)
            chunks_meta.append({
                "chunk_idx": idx,
                "time_duration": duration
            })
        logging.warning(chunks_meta)
        chunks_meta_n = list()
        for i in range(len(chunks_meta)):
            item_n = {**chunks_meta[i]}
            if i == 0:
                item_n["time_start"] = 0
            else:
                item_n["time_start"] = (chunks_meta_n[-1]["time_start"] 
                                        + chunks_meta_n[-1]["time_duration"])
            chunks_meta_n.append(item_n)
        return chunks_meta_n, os.path.join(self.destination_path, self.video_split_folder)

    def get_duration(self, path: str):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        video_duration = float(result.stdout)
        return video_duration
    

class Highlighter:
    def __init__(self, source_path: str, destination_path: str):
        self.source_path = source_path
        self.destination_path = destination_path
        self.video_duration = None
        self.video_split_folder = "video_split_highligher"
        self._prepare()

    def _prepare(self):
        assert os.path.isdir(self.destination_path)
        if os.path.exists(os.path.join(self.destination_path, self.video_split_folder)):
            shutil.rmtree(os.path.join(self.destination_path, self.video_split_folder))
        os.mkdir(os.path.join(self.destination_path, self.video_split_folder))

    def get_folder(self):
        return os.path.join(self.destination_path, self.video_split_folder)

    def get_highlights(self, hightlights_meta: list):
        text_file = list()
        for i, item in enumerate(hightlights_meta):
            os.system(
                ("ffmpeg "
                + f" -ss {item['time_start']} "
                + f" -i {self.source_path} "
                + f" -t {item['time_duration']} "
                + " -reset_timestamps 1 "
                + f" -c copy {os.path.join(self.destination_path, self.video_split_folder, f'{i}.mp4')}")
            )
            text_file.append("file" + " '" + os.path.join(self.destination_path, self.video_split_folder, f'{i}.mp4') + "' ")
