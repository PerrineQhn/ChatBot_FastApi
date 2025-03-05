from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import os
import datetime
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from ollama import chat
import pysolr
import static.open_app as open_app
from contextlib import asynccontextmanager
from pathlib import Path


# Connexion au core 'chatlogs' de Solr
solr = pysolr.Solr('http://localhost:8983/solr/chatlogs/', timeout=10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    open_app.start_solr()
    open_app.start_ollama()
    yield

app = FastAPI(lifespan=lifespan)

print("Working directory:", os.getcwd())
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# Historique global de la conversation (pour la démo)
conversation_context = []
question_reponse = []
question_reponse_file = BASE_DIR / "static/qa.json"

with open(question_reponse_file, "w") as f:
    json.dump([], f)

class QA(BaseModel):
    question: str
    reponse: str
    id: Optional[str] = None
    timestamp: Optional[str] = None

def safe_text(text):
    """
    Retourne le texte en s'assurant qu'il est correctement encodé en UTF-8.
    Les caractères invalides seront remplacés.
    """
    if isinstance(text, bytes):
        # Si c'est un objet bytes, on tente de le décoder
        return text.decode('utf-8', errors='replace')
    else:
        # On ré-encode et décode pour forcer le nettoyage
        return text.encode('utf-8', errors='replace').decode('utf-8')


def util_ajouter_QA(qa: QA):
    # Génération d'un ID unique et d'un timestamp
    qa.id = uuid4().hex
    qa.timestamp = datetime.datetime.now().isoformat() + "Z"

    qa.question = safe_text(qa.question)
    qa.reponse = safe_text(qa.reponse)

    json_qa = jsonable_encoder(qa)
    question_reponse.append(json_qa)

    # Sauvegarde dans le fichier JSON
    with open(question_reponse_file, "w") as f:
        json.dump(question_reponse, f, indent=4)
    
    # Préparation du document pour Solr
    document = {
        'id': qa.id,
        'question': qa.question,
        'reponse': qa.reponse,
        'timestamp': qa.timestamp
    }
    try:
        solr.add([document], commit=True)
        print("Document ajouté dans Solr :", document)
    except Exception as e:
        print("Erreur lors de l'ajout du document dans Solr :", e)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_bot(request: Request):
    form_data = await request.form()
    user_input = form_data.get('user_input')

    # Ajout du message utilisateur au contexte de conversation
    conversation_context.append({'role': 'user', 'content': user_input})
    # print("Contexte après ajout du message utilisateur :", conversation_context)
    
    # Appel du chatbot en transmettant l'intégralité du contexte
    stream = chat(
        model='llama3.2',
        messages=conversation_context,
        stream=False,
        options={"temperature": 0}
    )
    bot_response = stream.message.content

    # Ajout de la réponse du bot au contexte
    conversation_context.append({'role': 'assistant', 'content': bot_response})
    # print("Contexte après ajout de la réponse :", conversation_context)

    
    # Enregistrement de l'échange dans l'historique et indexation dans Solr
    temp_qa = QA(question=user_input, reponse=bot_response)
    util_ajouter_QA(temp_qa)

    return templates.TemplateResponse("chat.html", {"request": request, "donnee": question_reponse})
