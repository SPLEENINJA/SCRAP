import requests
from bs4 import BeautifulSoup
from datetime import datetime
import unicodedata 
import json
     
from pymongo import MongoClient


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def get_article_links(main_url):
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    articles = soup.find_all('article')
    for article in articles:
        a_tag = article.find('a')
        if a_tag and a_tag.get('href'):
            links.append(a_tag['href'])

    return links

def fetch_article_detail(article_url):
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        header = soup.find('header', class_='entry-header')
        print(f"header is {header}\n")
        title = header.find("h1", class_="entry-title").get_text(strip=True) if header else None
        summary = header.find("div", class_="article-hat").get_text(strip=True) if header else None
        author = header.find("span", class_="byline") if header else None
        # print(f"author is {author}\n")
        date = header.find("time", class_="entry-date") if header else None
        formatted_date = date.get('datetime') if date else None
        date_obj = datetime.fromisoformat(formatted_date).strftime("%d-%m-%Y")
        # print(f"date is {formatted_date}\n") #a formatter
        thumbnail = header.find("figure", class_="article-hat-img") if header else None
        image = thumbnail.find("img").get("src") if thumbnail and thumbnail.find("img") else None

        art = soup.find("div", class_='entry-content')
        content = [unicodedata.normalize('NFKC',tag.get_text(strip=True))
                   for tag in art.find_all()
                   if not tag.find() and tag.get_text(strip=True)] if art else []
        sous = soup.find("div",class_= 'meta-container').get_text(strip=True) if art else None
        abc = sous.split('Partager')[0]
        # print(abc)
         
        return {
            'titre': title,
            'résumé': summary,
            'auteur': author.get_text(strip=True),
            'date': date_obj,
            'image': image,
            'contenu': content,
            'url': article_url,
            'categories' : abc
        }

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du chargement de {article_url} : {e}")
        return None


# Lancement du scraping
main_url = "https://www.blogdumoderateur.com/web/"
article_links = get_article_links(main_url)
all_articles = []

for link in article_links:
    article_data = fetch_article_detail(link)
    # print(article_data)
    # print('\n')
    if article_data:
        all_articles.append(article_data)
    
with open("articles.json", "w", encoding="utf-8") as f: 
    data = json.dumps(all_articles, indent=2)
    data = json.dump(data, f)  # Valide si pas d'erreur
    # print("✅ JSON valide. Nombre d'articles :", len(data))


# # Connexion à MongoDB (localhost par défaut)
# client = MongoClient("mongodb://localhost:27017/")
# db = client["blog_scraping"]
# collection = db["articles"]

# # Charger les données JSON
# with open("articles.json", encoding="utf-8") as f:
#    data= json.dump(all_articles, f, ensure_ascii=False, indent=4)

# # Insertion dans la collection
# if isinstance(data, list):
#     collection.insert_many(data)
# else:
#     collection.insert_one(data)

# print("✅ Données insérées dans MongoDB.")

