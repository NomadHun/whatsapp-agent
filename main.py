from fastapi import FastAPI, Request
from fastapi.responses import Response
import json
import re
from gpt_engine import get_gpt_response
from rapidfuzz import process

app = FastAPI()

# Загружаем коллекции плитки
with open("products.json", encoding="utf-8") as f:
    products = json.load(f)

def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def find_product(message: str):
    message = normalize(message)

    # Точное совпадение по названию
    for product in products:
        name = normalize(product.get("Название", ""))
        if name == message:
            return product
        
    # Fuzzy matching
    names = [normalize(p.get("Название", "")) for p in products]
    match = process.extractOne(message, names, score_cutoff=80)
    if match:
        matched_name = match[0]
        return next((p for p in products if normalize(p.get("Название", "")) == matched_name), None)

    return None

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    message = form.get("Body")
    phone = form.get("From")

    # Пытаемся найти товар в products.json
    matched_product = find_product(message)
    print(f"Matched product: {matched_product}")
    gpt_reply, send_image = get_gpt_response(message, history=None, product=matched_product)
    image_url = matched_product.get("image_url") if matched_product else None

    # Отправка с фото
    if matched_product and send_image and image_url:
        return Response(content=f"""
<Response>
  <Message>
    <Body>{gpt_reply}</Body>
    <Media>{image_url}</Media>
  </Message>
</Response>
""", media_type="application/xml")

    # Отправка только текста
    return Response(content=f"""
<Response>
  <Message>
    <Body>{gpt_reply}</Body>
  </Message>
</Response>
""", media_type="application/xml")