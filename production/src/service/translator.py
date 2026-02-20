import re
import math
import torch
import logging
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer_ru_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
model_ru_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en").to(device)
tokenizer_en_ru = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
model_en_ru = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru").to(device)

class TranslatorRuEn:
    def __init__(self):
        self.tokenizer = tokenizer_ru_en
        self.model = model_ru_en

    def _prepare_texts(self, texts: str):
        logging.warning("processing::translation::prepare_texts")
        texts_hash = [re.sub("[^A-Za-z0-9]+", "", x).lower() for x in texts]
        hash2text = dict()
        for i, h in enumerate(texts_hash):
            if h not in hash2text:
                hash2text[h] = [i]
            else:
                hash2text[h].append(i)
        return hash2text, texts_hash, texts

    def _translate_texts(self, texts: str, batch_size: int = 64):
        logging.warning("processing::translation::translation::start")
        results = list()
        n_batches = math.ceil(len(texts) / batch_size)
        for i in tqdm(range(n_batches)):
            logging.warning(i)
            batch = texts[i*batch_size : (i+1)*batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
            inputs = {key: value.to(device) for key, value in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(**inputs)
            translations = self.tokenizer.batch_decode(outputs.cpu(), skip_special_tokens=True)
            results.extend(translations)
        logging.warning("processing::translation::translation::finish")
        return results

    def translate(self, texts: list):
        hash2text, text2hash, texts = self._prepare_texts(texts)
        hashes = list(hash2text.keys())
        texts_unique = list()
        for k, v in hash2text.items():
            texts_unique.append(texts[v[0]])
        logging.warning(texts_unique)
        texts_unique_tr = self._translate_texts(texts_unique)
        hash2texts_unique_tr = {h: tu_tr for h, tu_tr in zip(hashes, texts_unique_tr)}
        texts_tr = list()
        for h in text2hash:
            texts_tr.append(hash2texts_unique_tr[h])
        return texts_tr


class TranslatorEnRu:
    def __init__(self):
        self.tokenizer = tokenizer_en_ru
        self.model = model_en_ru

    def _prepare_texts(self, texts: str):
        logging.warning("processing::translation::prepare_texts")
        texts_hash = [re.sub("[^A-Za-z0-9]+", "", x).lower() for x in texts]
        hash2text = dict()
        for i, h in enumerate(texts_hash):
            if h not in hash2text:
                hash2text[h] = [i]
            else:
                hash2text[h].append(i)
        return hash2text, texts_hash, texts

    def _translate_texts(self, texts: str, batch_size: int = 64):
        logging.warning("processing::translation::translation::start")
        results = list()
        n_batches = math.ceil(len(texts) / batch_size)
        for i in tqdm(range(n_batches)):
            logging.warning(i)
            batch = texts[i*batch_size : (i+1)*batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
            inputs = {key: value.to(device) for key, value in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(**inputs)
            translations = self.tokenizer.batch_decode(outputs.cpu(), skip_special_tokens=True)
            results.extend(translations)
        logging.warning("processing::translation::translation::finish")
        return results

    def translate(self, texts: list):
        hash2text, text2hash, texts = self._prepare_texts(texts)
        hashes = list(hash2text.keys())
        texts_unique = list()
        for k, v in hash2text.items():
            texts_unique.append(texts[v[0]])
        texts_unique_tr = self._translate_texts(texts_unique)
        hash2texts_unique_tr = {h: tu_tr for h, tu_tr in zip(hashes, texts_unique_tr)}
        texts_tr = list()
        for h in text2hash:
            texts_tr.append(hash2texts_unique_tr[h])
        return texts_tr