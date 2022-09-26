# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from os import getcwd
# import requests
# from haystack.document_stores import ElasticsearchDocumentStore

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     doc_store = ElasticsearchDocumentStore(host = "es01", 
#                                         port = 9200, 
#                                         username = "", 
#                                         password = "", 
#                                         index = "naval2")

#     return {"message": "OK"}

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from os import getcwd

from . import schema, utils
#import schema, utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    pass

@app.get("/")
def read_root():
    return {"message": 'Hey!'}



@app.post("/question-file")
async def question_file(req: schema.QuestionOnly):
    question = req.question

    data = {"question":question,
        "context": 'context',
        "answer" : '42',
        "score": 100}

    return {"data": data}


@app.post("/upload_file")
async def upload_file(file: UploadFile):
    global FILE_PATH
    
    FILE_PATH = getcwd() + '/' + file.filename
    with open(FILE_PATH, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        buffer.close()

    text_stream = await utils.process_file(FILE_PATH)
    
    #haystack.process_for_elastic(text_stream)

    
    return {"filename": file.filename, "filepath":FILE_PATH, "rnd": text_stream[2]}