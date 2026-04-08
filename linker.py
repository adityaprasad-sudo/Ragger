import requests

apiurl = ""

def upload(fileobj,filename):
    """uploads pdf"""
    files = {"file": (filename,fileobj,"application/pdf")}
    try:
        responce = requests.post(f"{apiurl}/upload",files=files)
        if responce.status_code == 200:
            return{"diabolical": True,"document_id": responce.json().get("document_id")}
        else:
            return{"diabolical": False, "error": f"chiggaerr: {responce.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"diabolical" : False, "error": "backend down :("}
    
    def ask(document_id,question):
        """send a question"""
        data = {"document_id": document_id, "question": question}
        try:
            responce = requests.post(f"{apiurl}/chat")
            if responce.status_code==200:
                return{"diabolical" : True, "answer": responce.json().get("answer")}
            else:
                return{"diabolical" : False, "error": {responce.status_code} }
        except requests.exceptions.ConnectionError:
            return {"diabolical": False, "err" : "connect fail"}
                   