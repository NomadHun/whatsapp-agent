from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from gpt_engine import get_gpt_response
#from session_store import get_session, update_session
from crm_logger import log_interaction
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    phone = From.replace("whatsapp:", "")
    message = Body

    #history = get_session(phone)
    response = get_gpt_response(message, history)

    #update_session(phone, message, response)
    log_interaction(phone, message, response)

    return PlainTextResponse(response)