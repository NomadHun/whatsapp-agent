from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(message, history):
    messages = [{"role": "system", "content": "Ты — вежливый AI-ассистент по продажам керамогранита. Отвечай только на вопросы, связанные с продукцией. Если вопрос не по теме, напиши: 'Извините, я могу отвечать только по продукции QUASUN.'"}]

    for exchange in history:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["bot"]})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content