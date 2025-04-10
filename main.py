from fastapi import FastAPI, Request
from fastapi.responses import Response
import json
import re
from gpt_engine import get_gpt_response

app = FastAPI()

# Загружаем коллекции плитки
with open("products.json", encoding="utf-8") as f:
    products = json.load(f)

def find_product(message: str):
    message_lower = message.lower()
    for product in products:
        name = product.get("Название", "").lower()
        # Удаляем все лишние символы и разбиваем на слова
        name_keywords = re.findall(r"\w+", name)
        if any(keyword in message_lower for keyword in name_keywords):
            return product
    return None

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    message = form.get("Body")
    phone = form.get("From")

    # GPT формирует текст
    gpt_reply = get_gpt_response(message, history=None)

    # Пытаемся найти товар в products.json
    matched_product = find_product(message)
    print(f"Matched product: {matched_product}")
    image_url = matched_product.get("image_url") if matched_product else None

    # Отправка с фото
    if image_url:
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