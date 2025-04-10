import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загружаем данные из products.json
with open("products.json", "r", encoding="utf-8") as f:
    product_data = json.load(f)

# Сформируем краткий текст с описанием ассортимента
product_summary = "\n".join([
    f"{p['Название']} ({p['Размер']}, {p['Толщина']}, {p['Поверхность']}, {p['Страна-производитель']}, {p['Цена за кв. м']}₸)"
    for p in product_data[:30]  # первые 15 товаров
])

def get_gpt_response(message: str, history: list = None) -> str:
    messages = [
    {
        "role": "system",
        "content": (
          "Ты ассистент по продажам продукции QUASUN. Старайся отвечать кратко и без нагрузки на клиента. "
          "Твоя задача подготовить и довести клиента/лида до стадии продажи. "
          "Используй каталог ниже, чтобы предлагать плитку и помогать с выбором. "
            "Если пользователь просит 'обзор', 'рассказать про ассортимент' — приведи краткий список коллекций.\n\n"
            f"Вот товары:\n{product_summary}"
        )
    }
]   
    if history is None:
        history = []
    for exchange in history:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["bot"]})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content