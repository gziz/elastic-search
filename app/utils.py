import re
import PyPDF2
import os

def process_text(text):
  text = re.sub(pattern="\t", repl=' ', string=text)
  text = re.sub(pattern="\[[0-9]+\]", repl='', string=text)
  text = re.sub(pattern="\n-\n", repl='-', string=text)
  text = re.sub(pattern="(?<! )\n", repl=' ', string=text)
  text = re.sub(pattern="\n", repl='', string=text)
  text = re.sub(r"/^[A-Za-z\/\s\.'-]+$/", '', text)
  return text

def process_file(file_obj, file_path):

    # with open(file_path, "wb") as buffer:
    #     content = file_obj.read()
    #     buffer.write(content)
    #     buffer.close()

    # file_name, ext = os.path.splitext(file_path)

    # if ext == '.txt':
    #     pass

    # if ext == '.pdf':

    #     pdfFileObj = open(file_path, 'rb')
    #     # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(file_obj)

    text_stream = []
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        text = pageObj.extractText()
        text = process_text(text)

        text_stream.append(text)
        #with open(new_file_path, 'a') as f:
        #    f.write(text)
        
    return text_stream
    