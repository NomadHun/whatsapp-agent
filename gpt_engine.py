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
    f"{p['Название']} ({p['Размер']}, {p['Толщина']}, {p['Поверхность']}, {p['Страна-производитель']}, {p['Цена за кв. м']})"
    for p in product_data[:60]  # первые 15 товаров
])

def get_gpt_response(message: str, history: list = None, product=None) -> tuple[str, bool]:
    messages = [
        {
            "role": "system",
            "content": (
                "Ты ассистент по продажам продукции QUASUN. Старайся отвечать кратко и без нагрузки на клиента. "
                "Если пользователь интересуется визуальной частью товара (например, просит 'показать', 'фото', 'как выглядит', 'картинка') — добавь в конец ответа специальную метку [SEND_IMAGE], но не вставляй ссылку, URL или Markdown на изображение. "
                "Также учитывай, что некоторые товары могут иметь фотографии. "
                "Твоя задача подготовить и довести клиента/лида до стадии продажи. "
                "Используй каталог ниже, чтобы предлагать плитку и помогать с выборами. "
                "Если пользователь просит 'обзор', расскажи про ассортимент – приведи краткий список коллекций.\n\n"
                f"Вот товары:\n{product_summary} "
                "Если в ответе нужно отправить фото, добавь в самом конце метку [SEND_IMAGE] без дополнительных символов после неё (включая скобки, точки, кавычки и прочее). "
                "Никогда не вставляй ссылку на изображение в текст ответа. Фото отправляется отдельно через канал WhatsApp API. Только текст должен быть в ответе."
            )
        }
    ]

    if product:
        product_info = f"Информация о выбранном товаре: {product}. Не вставляй ссылку или Markdown на изображение."
        messages.append({
            "role": "system",
            "content": product_info
        })

        if "image_url" in product and product["image_url"]:
            messages.append({
                "role": "system",
                "content": (
                    "У этого товара также есть фотография. "
                    "Если пользователь просит показать или отправить фото, добавь метку [SEND_IMAGE]."
                )
            })

    if history is None:
        history = []

    for exchange in history:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["bot"]})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )

    full_text = response.choices[0].message.content.strip()
    send_image = full_text.strip().endswith("[SEND_IMAGE]")
    
    print("=== RAW GPT RESPONSE ===")
    print(full_text)
    print("========================")

    reply = full_text.replace("[SEND_IMAGE]", "").replace("SEND_IMAGE", "").replace("[]", "").strip()

    return reply, send_image