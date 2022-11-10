import itertools
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

def create_smaller_corpus(corpus: dict, qrels: dict, folder_path: str, number_thrash: int):
	usefull_documents_title = list(
		dict.fromkeys(itertools.chain.from_iterable(map(lambda x: list(x.keys()), qrels.values()))))
	useless_documents_title = list(set(corpus.keys()) - set(usefull_documents_title))
	final_corpus_titles = random.sample(useless_documents_title, number_thrash) + usefull_documents_title
	final_corpus_titles = list(filter(lambda x: x in corpus.keys(), final_corpus_titles))
	simple_corpus = {k: corpus[k] for k in final_corpus_titles}
	list_json = []
	for el in tqdm.tqdm(simple_corpus):
		list_json.append({el: simple_corpus[el]})
	print("Saving corpus")
	with open(os.path.join(folder_path, "dbpedia-entity", "corpus.jsonl"), "w") as file:
		for item in tqdm.tqdm(list_json):
			file.write(json.dumps(item) + "\n")
	return simple_corpus


