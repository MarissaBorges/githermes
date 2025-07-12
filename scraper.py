from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    pagina = navegador.new_page()
    pagina.goto("https://wiki.python.org/moin/BeginnersGuide")
    conteudo = pagina.content()

    links = []

    soup = BeautifulSoup(conteudo, 'html.parser')
    print(soup.prettify())
    for link in soup.find_all('a'):
        link = getattr(link, 'get', None)
        if link:
            links.append(link['href'])
        else:
            print("Link não possui um atributo get")
    
    markdown = md(conteudo)
    
    dados_site = {"links": links, "conteudo": markdown}

    print(dados_site)

  # return markdown