import datetime
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional
from uuid import uuid4

import pysolr
import static.open_app as open_app
from fastapi import FastAPI, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ollama import chat
from pydantic import BaseModel

# Connexion au core 'chatlogs' de Solr
solr = pysolr.Solr("http://localhost:8983/solr/chatlogs/", timeout=10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_app.start_solr()
    open_app.start_ollama()
    yield


app = FastAPI(lifespan=lifespan)

print("Working directory:", os.getcwd())
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# print("Templates directory:", templates.directory)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# Historique global de la conversation (pour la démo)
conversation_context = []
question_reponse = []
first_ajout_flag = True
question_reponse_file = BASE_DIR / "static/qa.json"


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
        return text.decode("utf-8", errors="replace")
    else:
        # On ré-encode et décode pour forcer le nettoyage
        return text.encode("utf-8", errors="replace").decode("utf-8")


def util_ajouter_QA(qa: QA):
    global first_ajout_flag
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

    if not first_ajout_flag:
        latest_doc = solr.search(q="*:*", sort="timestamp desc", rows=1)
        if latest_doc.hits > 0:
            doc_id = latest_doc.docs[0]['id'] 
            print(doc_id)
            solr.delete(id=doc_id)  # Suppression du dernier document
            solr.commit()  # Appliquer la suppression

    document = {
        "ids": [entry["id"] for entry in question_reponse],
        "questions": [entry["question"] for entry in question_reponse],
        "reponses": [entry["reponse"] for entry in question_reponse],
        "timestamp": [entry["timestamp"] for entry in question_reponse],
    }

    try:
        solr.add([document], commit=True)
        if first_ajout_flag:
            first_ajout_flag = False
        print("Document ajouté dans Solr :", document)
    except Exception as e:
        print("Erreur lors de l'ajout du document dans Solr :", e)


def recuperer_chatlogs():

    # Récupérer les 100 derniers documents
    chatlogs = solr.search("*:*", rows=100, sort="timestamp desc")
    last_log = next(iter(chatlogs), None)

    if last_log:
        return [
            {
                "ids": doc.get("ids"),
                "contents": [
                    [question, reponse]
                    for question, reponse in zip(
                        doc.get("questions"), doc.get("reponses")
                    )
                ],
                "time": "Date : " + doc.get("timestamp")[0].split("T")[0] + "\nTime : " + doc.get("timestamp")[0].split("T")[1].split('.')[0],
            }
            for doc in chatlogs
        ]
    else:
        return [
            {"ids": "", "contents": [["No history", "No history"]], "timestamps": ""}
        ]


@app.get("/chatlogs", response_class=HTMLResponse)
async def page_chatlogs(request: Request):
    return templates.TemplateResponse(
        "chatlogs.html", {"request": request, "logging": recuperer_chatlogs()}
    )


def vider_historique():
    solr.delete(q="*:*")  # '*' représente tous les documents
    solr.commit()  # Appliquer la suppression avec un commit
    question_reponse.clear()
    return [{"ids": "", "contents": [["No history", "No history"]], "timestamps": ""}]


@app.get("/clean_chatlogs", response_class=HTMLResponse)
async def page_chatlogs_no_logging(request: Request):
    return templates.TemplateResponse(
        "chatlogs.html", {"request": request, "logging": vider_historique()}
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ask", response_class=HTMLResponse)
async def askpage(request: Request):
    return templates.TemplateResponse(
        "chat.html", {"request": request, "donnee": question_reponse}
    )


@app.post("/ask")
async def ask_bot(request: Request):
    form_data = await request.form()
    user_input = form_data.get("user_input")

    # Ajout du message utilisateur au contexte de conversation
    conversation_context.append({"role": "user", "content": user_input})
    # print("Contexte après ajout du message utilisateur :", conversation_context)

    # Appel du chatbot en transmettant l'intégralité du contexte
    stream = chat(
        model="llama3.2",
        messages=conversation_context,
        stream=False,
        options={"temperature": 0},
    )
    bot_response = stream.message.content

    # Ajout de la réponse du bot au contexte
    conversation_context.append({"role": "assistant", "content": bot_response})
    # print("Contexte après ajout de la réponse :", conversation_context)

    # Enregistrement de l'échange dans l'historique et indexation dans Solr
    temp_qa = QA(question=user_input, reponse=bot_response)
    util_ajouter_QA(temp_qa)

    return templates.TemplateResponse(
        "chat.html", {"request": request, "donnee": question_reponse}
    )
