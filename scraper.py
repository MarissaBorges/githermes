from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    pagina = navegador.new_page()
    pagina.goto("https://wiki.python.org/moin/BeginnersGuide")
    conteudo = pagina.content()

    links = []

    soup = BeautifulSoup(conteudo, 'html.parser')
    print(soup.prettify())
    for elemento in soup.find_all('a'):
        if isinstance(elemento, Tag):
            if elemento.has_attr('href'):
                url = elemento['href']
                if "guide" in str(url).lower() or "docs" in str(url).lower():
                    links.append(url)
    
    markdown = md(conteudo)
    
    dados_site = {"links": links, "conteudo": markdown}

    print(dados_site)

  # return markdown