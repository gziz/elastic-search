from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

#import schema, utils
from . import schema, utils, haystack

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = 'secret')

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
async def question_file(req: schema.FileSchema):
    question = req.question
    #index, _ = os.path.splitext(req.file_name)
    index = 'naval'

    answers, documents = haystack.retrieve(question, index)

    data = {"question":question,
        "context": 'context',
        "answer" : '42',
        "score": 100}

    return {"ans": answers, 'docs': documents}


@app.post("/upload_file")
async def upload_file(file: UploadFile):
    
    FILE_PATH = os.getcwd() + '/' + file.filename

    text_stream = await utils.process_file(file, FILE_PATH)
    
    status = haystack.load_elastic(text_stream)
    status = 'ok'
    return {"filename": file.filename, "filepath":FILE_PATH, "status": status}