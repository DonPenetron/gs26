import logging

from .llm import (
    ClassifierModel,
    TrafficModel,
    FightModel,
    IndustrialModel,

    ClassifierModelCustom,
    CustomModel
)
# from .translator import TranslatorEnRu, TranslatorRuEn
from .grouper import Grouper

from utils import VLMModel


class MasterModel:
    def __init__(self, vlm_model: VLMModel):
        self.classifier_model = ClassifierModel(vlm_model)
        self.traffic_model = TrafficModel(vlm_model)
        self.fight_model = FightModel(vlm_model)
        self.industrial_model = IndustrialModel(vlm_model)

        self.classifier_model_custom = ClassifierModelCustom(vlm_model)
        self.custom_model = CustomModel(vlm_model)

        # self.translator_ru_en = TranslatorRuEn()
        # self.translator_en_ru = TranslatorEnRu()

        self.grouper = Grouper()

    def parse_video(self, video_filepath: str):
        logging.warning("processing::classification")
        event_type = self.classifier_model(video_filepath)
        logging.warning(event_type)

        logging.warning("processing::extraction")
        if event_type == "TRAFFIC":
            response = self.traffic_model(video_filepath)
        elif event_type == "FIGHT":
            response = self.fight_model(video_filepath)
        elif event_type == "INDUSTRIAL":
            response = self.industrial_model(video_filepath)
        else:
            response = []
        logging.warning(response)

        logging.warning("processing::translation")
        descriptions = list()
        for item in response:
            if item.get("description") is not None:
                descriptions.append(item.get("description"))
            else:
                descriptions.append(" ")
        # descriptions_tr = self.translator_en_ru.translate(descriptions)
        descriptions_tr = descriptions
        logging.warning(descriptions_tr)

        logging.warning("processing::encoding")
        result = list()
        for i, item in enumerate(response):
            item_n = {
                "event_type": event_type 
            }
            for k, v in item.items():
                if k == "timestamp":
                    try:
                        float(v)
                        item_n["time_start"] = v
                    except:
                        break
                elif k == "description":
                    item_n["description"] = descriptions_tr[i]
                elif k == "duration":
                    try:
                        float(v)
                        item_n["time_duration"] = v
                    except:
                        item_n["time_duration"] = "5"
                elif k == "confidence":
                    try:
                        float(v)
                        item_n["confidence"] = v
                    except:
                        item_n["confidence"] = "0.5"
            if "time_duration" not in item_n:
                item_n["time_duration"] = "3"
            if "confidence" not in item_n:
                item_n["confidence"] = "0.5"
            logging.warning(item_n)
            if item_n.get("time_start") is None:
                continue
            result.append(item_n)

        results_dedup = self.grouper.deduplicate_sequence(result)

        return results_dedup
    
    def parse_video_custom(self, video_filepath: str, description: str):
        logging.warning("starting::parse_video_custom")

        # description_tr = self.translator_ru_en.translate([description])[0]
        description_tr = description
        logging.warning("processing::classification")
        flag = self.classifier_model_custom(video_filepath, description_tr)
        logging.warning(flag)

        logging.warning("processing::extraction")
        if not flag:
            return []
        response = self.custom_model(video_filepath, description_tr)
        logging.warning(response)

        logging.warning("processing::translation")
        descriptions = list()
        for item in response:
            if item.get("description") is not None:
                descriptions.append(item.get("description"))
            else:
                descriptions.append(" ")
        # descriptions_tr = self.translator_en_ru.translate(descriptions)
        descriptions_tr = descriptions
        logging.warning(descriptions_tr)

        logging.warning("processing::encoding")
        result = list()
        for i, item in enumerate(response):
            item_n = {
                "event_type": "CUSTOM" 
            }
            for k, v in item.items():
                if k == "timestamp":
                    try:
                        float(v)
                        item_n["time_start"] = v
                    except:
                        break
                elif k == "description":
                    item_n["description"] = descriptions_tr[i]
                elif k == "duration":
                    try:
                        float(v)
                        item_n["time_duration"] = v
                    except:
                        item_n["time_duration"] = "3"
                elif k == "confidence":
                    try:
                        float(v)
                        item_n["confidence"] = v
                    except:
                        item_n["confidence"] = "0.5"
            if "time_duration" not in item_n:
                item_n["time_duration"] = "3"
            if "confidence" not in item_n:
                item_n["confidence"] = "0.5"
            logging.warning(item_n)
            if item_n.get("time_start") is None:
                continue
            result.append(item_n)

        results_dedup = self.grouper.deduplicate_sequence(result)

        return results_dedup