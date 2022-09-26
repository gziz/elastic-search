from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
BERT_MODEL_PATH = BASE_DIR / "ai-models" / "bert-base-cased-squad2"

reader = FARMReader(model_name_or_path=BERT_MODEL_PATH)


def process_for_elastic(text_stream):
    data_json = [
      {'content': paragraph,
        'meta': {'source': 'naval'}}
         for paragraph in text_stream
      ]
    return data_json


def load_elastic(text_stream):

    data_json = process_for_elastic(text_stream)

    doc_store = ElasticsearchDocumentStore(host = "es01", 
                                    port = 9200, 
                                    username = "", 
                                    password = "", 
                                    index = "naval")

    doc_store.write_documents(data_json)
    return 'OK'


def get_document_store(index: str):
    document_store = ElasticsearchDocumentStore(host = "es01", 
                                                port = 9200, 
                                                username = "", 
                                                password = "", 
                                                index = index)
    return document_store


def retrieve(index, query):
    document_store = get_document_store(index)
    retriever = BM25Retriever(document_store=document_store)
    pipe = ExtractiveQAPipeline(reader, retriever)

    predictions = pipe.run(
      query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}}
    )
    predictions = [ans.answer for ans in predictions['answers']]
    return predictions