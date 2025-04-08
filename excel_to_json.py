import pandas as pd
import json

# Загрузка Excel
df = pd.read_excel("quasun_keramogranit_catalog_complete.xlsx")

# Пример отбора нужных колонок (проверь названия по своему файлу!)
df = df[["Название", "Размер", "Толщина", "Поверхность", "Страна-производитель", "Цена за кв. м"]]

# Преобразуем в список словарей
products = df.to_dict(orient="records")

# Сохраняем как JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("✅ products.json создан.")