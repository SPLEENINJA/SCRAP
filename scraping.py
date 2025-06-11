
import requests
from bs4 import BeautifulSoup

m_url = "https://www.blogdumoderateur.com/web/"
article_links = get_article_links(m_url)
all_articles = []

def fetch_article_detail(article_url):
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        header = soup.find('header', class_='entry-header')
        title = header.find("h1", class_="entry-title").text.strip() if header else None
        summary = header.find("div", class_="article-hat").text.strip() if header else None
        author = header.find("a", class_="byline").get('title') if header else None
        date = header.find("time", class_="posted-on").get('datetime') if header else None

        thumbnail = header.find("figure", class_="article-hat-img") if header else None
        image = thumbnail.find("img").get("src") if thumbnail and thumbnail.find("img") else None

        art = soup.find("div", class_='entry-content')
        content = [tag.get_text(strip=True)
            for tag in art.find_all()
            if not tag.find() and tag.get_text(strip=True)] if art else []

        return {
        'titre': title,
        'résumé': summary,
        'auteur': author,
        'date': date,
        'image': image,
        'contenu': content,
        'url': article_url
        }

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du chargement de {article_url} : {e}")
        return None

def get_article_links(m_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(m_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for article in soup.find_all('article'):
        a_tag = article.find('a')
        if a_tag and a_tag.get('href'):
            links.append(a_tag['href'])

    return links

for link in article_links:
    article_data = fetch_article_detail(link)
    if article_data:
        all_articles.append(article_data)

print(all_articles)


def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles_data = [] 

#request http > url >html > soup > soup.obj 
        #main article soup.find(body of article) (div.post-content) 
            #content header (header.entry-header)
                #title (entry-title)  
                #summary (div.article-hat)
                #author (byline)
                #date (posted-on) if time if datetime format return none 
                #thumbnail (figure.article-hat-img) src & srcset (attention srcset a nettoyer) 
            #entry content (div entry-content)
                #content ()
                #images (figure)
                #sub categories

        header=soup.find('header', class_='entry-header')
        title = header.find("h1", class_="entry-title") 
        summary= header.find("div", class_="article-hat") 
        author=header.find("a",class_="byline").get('title')
        date=header.find("time", class_="posted-on").get('datetime')
        thumbnail=header.find("figure", class_="article-hat-img")
        header.find("figure", class_="article-hat-img").get('src') if thumbnail else None
        art=soup.find("div",class_='entry-content')
        content=[tag.get_text(strip=True)
        for tag in art.find_all()
        if not tag.find() and tag.get_text(strip=True)]
        print(content)    
        cate=art.find("li",class_= "post-tags")
                       
        articles_data.append(
            {'titre' : title,
            'résumé' : summary,
            'auteur' : author,
            'date' : date,
            'image' : thumbnail}
        )
        return articles_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    
    




