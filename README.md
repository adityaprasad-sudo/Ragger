## What is Ragger?
**Ragger** is an open source custom built **pipeline** which lets you **upload pdfs** and have you ask questions about that pdf from the AI model.
These Pdfs can include anything from **Legal Contracts & Policies**, **Academic & Scientific Papers**, **Tech Manuals & Documentation** ,
**etc.**

## How did i make it
1. ### Webpage(The frontend)
- The webpage is fully built from scratch using Html, CSS and javascript.
2. ### The Backend
- The is backend is built on python and is hosted on **Hugging Face(using docker and uvicorn)** you access the Hugging face space from [here](https://huggingface.co/spaces/AmbitiousPotato/Ragger/tree/main)

## Requirements
The project requires the following libraries:-

 1. fastapi
   2. uvicorn
    3. python-multipart
      4. langchain
       5. langchain-community
   6.    langchain-openai
     7.   langchain-core
      8.  langchain-text-splitters
     9.   pypdf
     10.   faiss-cpu
       11. python-dotenv

**Quick install**

    pip install fastapi uvicorn python-multipart langchain langchain-community langchain-openai langchain-core langchain-text-splitters pypdf faiss-cpu python-dotenv
     
## Want to Contribute
Are you looking forward to contribute i would love that TBH the webpage isnt very beautiful sooo you can make your custom webpage and Showcase it [here](https://github.com/adityaprasad-sudo/Ragger/discussions)

## Want to rebuild it locally
Sure! Here are the steps:-
1. Download the backend.py file from the repo.
2. Use hugging face or similar webpage to host the backend and obtain an public apiurl.
       i. you can test if the backend is working or not by using the generated url if you are using fastapi then apiurl/docs will let you try the backend first. 
3. make/download the frontend from the repo and use javascript to link the frontend to the backend.
4. After linking both the frontend and backend the pipeline should work properly.
## Screenshots

<img width="1279" height="892" alt="Screenshot 2026-04-09 114327" src="https://github.com/user-attachments/assets/febd8c57-c214-4101-928e-a6a0d09e6379" />
<img width="1279" height="891" alt="Screenshot 2026-04-09 114228" src="https://github.com/user-attachments/assets/9ed3120f-db0e-479c-b79f-1470904db914" />


