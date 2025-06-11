from pymongo import MongoClient
import json

# Connexion à MongoDB (localhost par défaut)
client = MongoClient("mongodb://localhost:27017/")
db = client["blog_scraping"]
collection = db["articles"]

# Charger les données JSON
with open("articles.json", encoding="utf-8") as f:
   data= json.dump(all_articles, f, ensure_ascii=False, indent=4)

# Insertion dans la collection
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("✅ Données insérées dans MongoDB.")