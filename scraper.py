from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import os
from pprint import pprint

def verificar_https(url):
    url_analisada = urlparse(url)
    if not url_analisada.scheme:
        print(f"URL '{url}' não tem esquema. Adicionando 'https://' como padrão.")
        url_limpa = 'https://' + url
        return url_limpa
    return url

def verificar_url_absoluto(url_base, url):
    url_absoluta = urljoin(url_base, url)
    return url_absoluta

def extrair_conteudo_e_links_do_site(pagina, url):
    try:
        pagina.goto(url, wait_until="domcontentloaded", timeout=15000)
        conteudo = pagina.content()
        print("conteúdo da página extraído")

        links = []
        markdown = []

        soup = BeautifulSoup(conteudo, 'lxml')
        for elemento in soup.find_all('a'):
            if isinstance(elemento, Tag):
                if elemento.has_attr('href'):
                    url = elemento['href']
                    if "guide" in str(url).lower() or "docs" in str(url).lower():
                        links.append(url)

        markdown = md(conteudo)
        print("convertendo o conteúdo em markdown")
    except Exception as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")

    return {"links": links, "conteudo": markdown}

def baixar_documentacao(nome_colecao, nome_arquivo, conteudo_markdown):
    caminho_colecao = f"data/collections/{nome_colecao}"
    print(f"Baixando conteúdo no caminho: {caminho_colecao}")
    os.makedirs(caminho_colecao, exist_ok=True)
    with open(f"{caminho_colecao}/{nome_arquivo}.md", 'w', encoding="utf-8") as file:
        file.write(conteudo_markdown)
        print(f"Conteúdo da página salvo com sucesso. Caminho: {caminho_colecao}/{nome_arquivo}.md\n\n")

def gerenciar_dados_da_pagina(nome_colecao, url):
    print("Iniciando o processo...")
    url = verificar_https(url)
    urls_vistas = []
    urls_para_acessar = []
    if url not in urls_para_acessar:
        urls_para_acessar.append(url)
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)
        pagina = navegador.new_page()
        print("pagina criada")
        while urls_para_acessar:
            url_atual = urls_para_acessar.pop(0)
            if url_atual in urls_vistas:
                continue
            print(f"\n\nVerificando a url: {url_atual}")
            parser = urlparse(url_atual)
            dominio = parser.hostname
            caminho = parser.path
            dominio_e_caminho = dominio + caminho
            nome_arquivo = "".join(["_" if caracter in "/?:-" else caracter for caracter in dominio_e_caminho ])
            print(f"\n{nome_arquivo}")
            urls_vistas.append(url_atual)
            dados_pagina_atual = extrair_conteudo_e_links_do_site(pagina, url_atual)
            print(f"dados extraídos")
            if dados_pagina_atual:
                novos_links = dados_pagina_atual["links"]
                conteudo_markdown = dados_pagina_atual["conteudo"]
                print(f"Novos links capturados:\n{novos_links}")
                for link in novos_links:
                    if link not in urls_vistas:
                        urls_para_acessar.append(verificar_url_absoluto(url_atual, link))
                baixar_documentacao(
                nome_arquivo=nome_arquivo,
                nome_colecao=nome_colecao,
                conteudo_markdown=conteudo_markdown
                )
            else:
                print("A página não possui dados ou não foi carregada")

    return {"urls_vistas": urls_vistas, "urls_para_acessar": urls_para_acessar}

pprint(gerenciar_dados_da_pagina(
  nome_colecao="python_docs",
  url="https://docs.python.org/3/index.html"
))