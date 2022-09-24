from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import getcwd
import requests
from haystack.document_stores import ElasticsearchDocumentStore

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
    doc_store = ElasticsearchDocumentStore(host = "localhost", 
                                        port = 9200, 
                                        username = "", 
                                        password = "", 
                                        index = "naval2")

    return {"message": "OK"}

