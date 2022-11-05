import beir

from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

#Dowload DBPedia entity dataset
dbpedia = GenericDataLoader(root_dir="data", dataset="dbpedia")
queries, corpus, qrels = dbpedia.load(split="test")
