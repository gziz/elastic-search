from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from os import getcwd

#import schema, utils
from . import schema, utils#, haystack

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
    text_stream = await utils.process_file(file, FILE_PATH)
    
    #haystack.process_for_elastic(text_stream)

    
    return {"filename": file.filename, "filepath":FILE_PATH, "rnd": text_stream}