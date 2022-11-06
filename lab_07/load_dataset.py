import os.path

import beir
from beir import util

import tqdm
import random
import json
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES


def download_dataset(folder_path: str):
	url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/dbpedia-entity.zip"
	data_path = util.download_and_unzip(url, folder_path)
	corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")
	return corpus, queries, qrels


def create_smaller_corpus(corpus: dict, queries, qrels: dict, folder_path: str, number_themes: int):
	set_usefull_themes = set()
	for q in qrels:
		for t in qrels[q]:
			set_usefull_themes.add(t)
	obj = set([el for el in tqdm.tqdm(corpus)])
	obj = obj.difference(set_usefull_themes)
	trash_themes = random.sample(obj, k=number_themes)
	set_usefull_themes = set_usefull_themes.union(trash_themes)
	corpus2 = {key: value for (key, value) in corpus.items() if key in set_usefull_themes}
	list_json = []
	print("Create list_json")
	for el in tqdm.tqdm(corpus2):
		list_json.append(
			{"_id": el, "title": el[9:-1], "text": corpus2[el],
				"metadata": f"<http://dbpedia.org/resource/{el[9:-1]}>"})
	print("Saving corpus")
	with open(os.path.join(folder_path, "dbpedia-entity", "corpus.jsonl"), "w") as file:
		for item in tqdm.tqdm(list_json):
			file.write(json.dumps(item) + "\n")
	return corpus2
