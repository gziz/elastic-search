from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import getcwd
import requests
#from haystack.document_stores import ElasticsearchDocumentStore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    res = requests.get('http://localhost:9200/_cat/indices').text
    return {"message": res}

