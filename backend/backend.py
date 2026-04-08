import os
from fastapi import FastAPI, UploadFile,File,Form
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import tempfile
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
hcapi = os.getenv("OPENAI_API_KEY")
hcurl = "https://ai.hackclub.com/proxy/v1"

llm = ChatOpenAI(
    model = "google/gemini-2.5-flash",
    api_key= hcapi,
    base_url= hcurl,
)

embeddings = OpenAIEmbeddings(
    model = "openai/text-embedding-3-large",
    api_key=hcapi,
    base_url=hcurl,
)
@app.post("/upload")
async def uploadpdf(file: UploadFile = File(...)):
    '''Handles pdf uploads,chunking and creates faiss databaseee'''
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        tmpfile.write(await file.read())
        tmppath = tmpfile.name
    try:
        loader = PyPDFLoader(tmppath)
        docs = loader.load()
        textsplitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )
        splits = textsplitter.split_documents(docs)
        vectorstore = FAISS.from_documents(splits, embeddings)
        folder_path = f"./faiss_indexes/{file.filename}"
        vectorstore.save_local(folder_path)
        return {"msg": "pdfuploaded", "document_id": file.filename}
    finally:
        os.remove(tmppath)
@app.post("/chat")
async def chatpdf(documentid: str = Form(...), question: str = Form(...)):
    """Retrieves relevant chunks and gives an answer using the text model"""
    
    folderpath = f"./faiss_indexes/{documentid}"
    
    if not os.path.exists(folderpath):
        return {"error": "notfound"}
        
    vectorstore = FAISS.load_local(
       folderpath,
       embeddings,
       allow_dangerous_deserialization=True
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    template = """answer the question only on the following context:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def formatdocs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    ragchain = (
        {
            "context": retriever | formatdocs, 
            "question": RunnablePassthrough()
        } 
        | prompt 
        | llm 
        | StrOutputParser()
    )
    responce = ragchain.invoke(question)
    return {"ans": responce}
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app,host="127.0.0.1",port=8000)



