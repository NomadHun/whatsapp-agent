import os
import json

assets_folder = "assets"
base_url = "https://raw.githubusercontent.com/NomadHun/whatsapp-agent/main/assets"

# Получаем список файлов из assets/
asset_files = os.listdir(assets_folder)
asset_map = {os.path.splitext(f)[0].lower(): f for f in asset_files}

# Загружаем продукты
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Обновляем продукты с image_url
for product in products:
    slug = product["Название"].lower().replace(" ", "_")
    if slug in asset_map:
        product["image_url"] = f"{base_url}/{asset_map[slug]}"

# Сохраняем обратно
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)