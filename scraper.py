from playwright.sync_api import sync_playwright, Error, TimeoutError
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import os
from pprint import pprint
import json
import tldextract
from time import time

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

def carregar_config_urls(caminho_do_arquivo="config_urls.json"):
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de configuração '{caminho_do_arquivo}' não encontrado.")
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{caminho_do_arquivo}' tem um erro de sintaxe JSON.")
    return {}

def extrair_dominio_principal(url_completa):
    partes_extraidas = tldextract.extract(url_completa)
    return partes_extraidas.top_domain_under_public_suffix

def extrair_dados_da_pagina(pagina, url):
    try:
        pagina.goto(url, wait_until="domcontentloaded", timeout=15000)
        conteudo = pagina.content()
        print("conteúdo da página extraído")

        links = []
        markdown = []

        soup = BeautifulSoup(conteudo, 'lxml')
        for elemento in soup.find_all('a', href=True):
            if isinstance(elemento, Tag):
                if elemento.has_attr('href'):
                    links.append(url)

        markdown = md(conteudo)
        print("convertendo o conteúdo em markdown")
        return {"links": links, "conteudo": markdown}
    except TimeoutError as e:
        print(f"FALHA ESPECÍFICA: Timeout ao acessar {url}. {e}")
        return "TimeoutError"
    except Error as e:
        print(f"Ocorreu um erro de Playwright/Rede ao acessar {url}: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")
        return None

def baixar_conteudo(nome_colecao, nome_arquivo, conteudo_markdown):
    try:
        caminho_colecao = f"data/collections/{nome_colecao}"
        print(f"Baixando conteúdo no caminho: {caminho_colecao}")
        os.makedirs(caminho_colecao, exist_ok=True)
        with open(f"{caminho_colecao}/{nome_arquivo}.md", 'w', encoding="utf-8") as file:
            file.write(conteudo_markdown)
            print(f"Conteúdo da página salvo com sucesso. Caminho: {caminho_colecao}/{nome_arquivo}.md\n\n")
    except (OSError, IOError, TypeError) as e:
        print(f"ERRO CRÍTICO ao salvar o arquivo {nome_arquivo}: {e}")

def gerenciar_dados_da_pagina(nome_colecao, url):
    config = carregar_config_urls()

    DOMINIOS_CONFIAVEIS = config.get("mapa_de_vizinhancas", {})
    PREFIXOS_DE_CAMINHO_PERMITIDOS = set(config.get("prefixos_de_caminho_permitidos", []))
    EXTENSOES_PROIBIDAS = set(config.get("extensoes_proibidas", []))
    SEGMENTOS_DE_CAMINHO_PROIBIDOS = set(config.get("segmentos_de_caminho_proibidos", []))
    PROTOCOLOS_PROIBIDOS = set(config.get("protocolos_proibidos", []))

    print("Iniciando o processo...")
    url = verificar_https(url)

    urls_vistas = []
    urls_para_acessar = []
    urls_rejeitadas = []

    if url not in urls_para_acessar:
        urls_para_acessar.append(url)

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)
        pagina = navegador.new_page()
        print("pagina criada")

        dominio_principal = extrair_dominio_principal(url)

        dominios_permitidos = set() 

        if dominio_principal in DOMINIOS_CONFIAVEIS:
            dominios_permitidos = DOMINIOS_CONFIAVEIS[dominio_principal]
            print(f"INFO: Usando escopo amplo para a vizinhança conhecida: {dominio_principal}")
        else:
            dominio_exato = urlparse(url).hostname
            dominios_permitidos.add(dominio_exato)
            print(f"INFO: Usando escopo restrito para o domínio: {dominio_exato}")

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

            dados_pagina_atual = extrair_dados_da_pagina(pagina, url_atual)

            print(f"dados extraídos")

            if dados_pagina_atual:
                novos_links = dados_pagina_atual["links"]
                conteudo_markdown = dados_pagina_atual["conteudo"]
                print(f"Novos links capturados:\n{novos_links}")

                for link in novos_links:
                    link_absoluto = verificar_url_absoluto(url_atual, link)
                    parsed_url = urlparse(link_absoluto)
                    url_limpa = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

                    if not link_absoluto or link_absoluto.startswith('#') or url_limpa in urls_vistas or url_limpa in urls_para_acessar:
                        continue

                    parsed_url = urlparse(url_limpa)
                    dominio_do_link = parsed_url.hostname
                    if dominio_do_link not in dominios_permitidos:
                        urls_rejeitadas.append(url_limpa)
                        continue

                    caminho_do_link = (parsed_url.path or "/").lower()
                    if not any(caminho_do_link.startswith(prefixo) for prefixo in PREFIXOS_DE_CAMINHO_PERMITIDOS):
                        urls_rejeitadas.append(url_limpa)
                        continue

                    if any(link_absoluto.startswith(protocolo) for protocolo in PROTOCOLOS_PROIBIDOS):
                        urls_rejeitadas.append(link_absoluto)
                        continue

                    if any(caminho_do_link.endswith(ext) for ext in EXTENSOES_PROIBIDAS):
                        urls_rejeitadas.append(url_limpa)
                        continue

                    if any(item_proibido in url_limpa.lower() for item_proibido in SEGMENTOS_DE_CAMINHO_PROIBIDOS):
                        urls_rejeitadas.append(url_limpa)
                        continue

                    urls_para_acessar.append(verificar_url_absoluto(url_atual, link))
                baixar_conteudo(
                nome_arquivo=nome_arquivo,
                nome_colecao=nome_colecao,
                conteudo_markdown=conteudo_markdown
                )
            else:
                print("A página não possui dados ou não foi carregada")

    return {"urls_vistas": urls_vistas, "urls_para_acessar": urls_para_acessar, "urls_rejeitadas": urls_rejeitadas}

if __name__ == "__main__":
    tempo_inicio = time()

    pprint(gerenciar_dados_da_pagina(
    nome_colecao="python_docs",
    url="https://docs.python.org/3/index.html"
    ))

    tempo_execucao = time() - tempo_inicio
    print(f"O programa levou {tempo_execucao:.2f} segundos para executar")