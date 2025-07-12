from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
import os

def verificar_https(url):
  if not "https" in url:
    return "https://" + url

def extrair_conteudo_e_links_do_site(url):
    url = verificar_https(url)
    if url:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch(headless=False)
            pagina = navegador.new_page()
            pagina.goto(url)
            conteudo = pagina.content()

            links = []
            try:
                soup = BeautifulSoup(conteudo, 'html.parser')
                for elemento in soup.find_all('a'):
                    if isinstance(elemento, Tag):
                        if elemento.has_attr('href'):
                            url = elemento['href']
                            if "guide" in str(url).lower() or "docs" in str(url).lower():
                                links.append(url)
            except Exception as e:
                print(f"Ocorreu um erro ao extrair os links: {e}")
            
            markdown = md(conteudo)

            dados_site = {"links": links, "conteudo": markdown}
    return dados_site

def baixar_documentacao(url):
    urls_ja_vistas = set()
    urls_para_acessar = []

    if url not in urls_para_acessar:
        urls_para_acessar.append(url)

    while urls_para_acessar:
        url_atual = urls_para_acessar.pop(0)

        if url_atual in urls_ja_vistas:
            continue

        dados_site = extrair_conteudo_e_links_do_site(url_atual)
        links = dados_site['links']
        conteudo = dados_site['conteudo']

        for link in links:
            if link not in urls_ja_vistas:
                urls_para_acessar.append(link)
        urls_ja_vistas.add(url_atual)

    return {"urls_ja_vistas": urls_ja_vistas, "urls_para_acessar": urls_para_acessar}

print(baixar_documentacao("https://wiki.python.org/moin/FrontPage"))