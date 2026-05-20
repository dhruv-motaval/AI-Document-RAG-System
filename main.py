from fastapi import FastAPI, UploadFile, File ,HTTPException,status
import os
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
import re
from pydantic import BaseModel
import ollama
import uuid



app = FastAPI()

UPLOAD_DIR = 'uploads'

os.makedirs(UPLOAD_DIR,exist_ok=True)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection( name = 'document_collection')

class QuestionRequest(BaseModel):
    question : str

def clean_text(text):

    text = re.sub(r'\s+',' ',text)
    
    return text

def extract_text(file_path):
    
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        
        doc = fitz.open(file_path)

        text=""

        for page in doc:
            text += page.get_text()

        return text
    elif file_extension == '.txt':
        with open(file_path,'r',encoding='utf-8') as f:
            return f.read()
        
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Unsupported file Type')

def chunk_text(text,chunk_size=500,overlap =100):
    chunks=[]

    start =0

    # for i in range(0,len(text),chunk_size):
    #     chunk = text[i:i+chunk_size]
    #     chunks.append(chunk)

    while start< len(text):
        end = start + chunk_size

        chunks.append(text[start:end])
        start +=chunk_size-overlap

    return chunks


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):

    allowed_extension = ['.pdf','.txt']

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Upload PDF file or Text File'
        )



    file_path = os.path.join(UPLOAD_DIR,file.filename)

    with open(file_path, 'wb') as f:
        f.write(await file.read())
    try:
        text = extract_text(file_path)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid or corrupted Document'
        )

    text=clean_text(text)

    chunks =chunk_text(text)

    for i,chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            documents = [chunk],
            embeddings = [embedding],
            metadatas=[{"filename": file.filename}],
            ids =[str(uuid.uuid4())]
        )
    
    return {
        'filename' : file.filename,
        'text_preview': text[:500],
        'total_chunks' : len(chunks),
        'message' : 'Embeddings Stored successfully'
    }

@app.post('/ask')
async def ask_question(data: QuestionRequest):
    question_embedding = embedding_model.encode(data.question).tolist()

    results = collection.query(query_embeddings=[question_embedding], n_results=3)

    context = '\n'.join(results['documents'][0])

    prompt = f""" Answer the question using only the context below.

    If answer is not present,say:
    'I could Not find that information in the document'

    context:
    {context}

    question:
    {data.question}
    """

    response = ollama.chat(model="llama3.1",
                           messages=[
                               {'role':'user',
                                'content' : prompt}
                           ])

    return {'answer' : response['message']['content']}