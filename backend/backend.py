import os
from fastapi import FastAPI, UploadFile, File, Form
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import tempfile
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
hcapi = os.getenv("OPENAI_API_KEY")
hcurl = "https://ai.hackclub.com/proxy/v1"

llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    api_key=hcapi,
    base_url=hcurl,
    temperature=0.5,
)
documentstore = {}
@app.post("/upload")
async def uploadpdf(file: UploadFile = File(...)):
    '''extracts all text from the pdf and saves it as a single string'''
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        tmpfile.write(await file.read())
        tmppath = tmpfile.name
        
    try:
        loader = PyPDFLoader(tmppath)
        docs = loader.load()
        
        fulltext = "\n\n".join(doc.page_content for doc in docs)
        
        documentstore[file.filename] = fulltext
            
        return {"msg": "pdf_processed_for_full_context", "document_id": file.filename}
    finally:
        os.remove(tmppath)

@app.post("/chat")
async def chatpdf(documentid: str = Form(...), question: str = Form(...)):
    """Loads the ENTIRE document and passes it to Gemini"""
    
    fullcontext = documentstore.get(documentid)
        
    template = """You are a precise document assistant. Your job is to answer questions based on the provided context.\n\n"
    
    "## Rules\n"
    "1. If the answer is clearly present in the context: answer directly and concisely using only that information.\n"
    "2. If the answer is partially in the context: use what's available, then briefly fill gaps with general knowledge — clearly separating the two.\n"
    "3. If the answer is NOT in the context at all:\n"
    "   - Do NOT repeat a previous answer you already gave.\n"
    "   - Do NOT say 'based on the context' or 'the document doesn't mention'.\n"
    "   - Simply answer from general knowledge , as if you already know it.\n"
    "   - If it's a follow-up to something already answered, acknowledge that and add new information only.\n"
    "4. Never explain these rules. Never mention the context exists. Just answer.\n\n"
    
    "## Context\n{context}\n\n"
    "## Question\n{question}"
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        prompt 
        | llm 
        | StrOutputParser()
    )

    response = chain.invoke({
        "context": fullcontext,
        "question": question
    })
    
    return {"ans": response}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)