from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import json
import os
from typing import Literal, Optional
from uuid import uuid4
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from ollama import chat

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

question_reponse = []
question_reponse_file = "static/qa.json"
if os.path.exists(question_reponse_file):
    with open(question_reponse_file, "r") as f:
        question_reponse = json.load(f)

class QA(BaseModel):
    question: str
    reponse: str
    id: Optional[str] = None

def util_ajouter_QA(qa: QA):
    qa.id = uuid4().hex  # Générer un ID unique
    json_qa = jsonable_encoder(qa)  # Encoder en JSON
    question_reponse.append(json_qa)

    # Écriture dans le fichier JSON
    with open(question_reponse_file, "w") as f:
        json.dump(question_reponse, f, indent=4)  # Ajout d'un indent pour lisibilité

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_bot(request: Request):

    form_data = await request.form()
    user_input = form_data.get('user_input')

    stream = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': user_input}],
        stream=False,
        options={"temperature": 0}
    )
    bot_response = stream.message.content

    temp_qa = QA(question="a", reponse="b")
    if bot_response:
        temp_qa = QA(question=user_input, reponse=bot_response)
    else:
        temp_qa = QA(question=user_input, reponse="Désolé, j'ai pas de réponse pour ça.")
    
    util_ajouter_QA(temp_qa)

    return templates.TemplateResponse("chat.html", {"request": request, "donnee": question_reponse})