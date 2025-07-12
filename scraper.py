from playwright.sync_api import sync_playwright, Error, TimeoutError
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import os
from pprint import pprint
import json
import tldextract
from time import time
from dotenv import load_dotenv, find_dotenv
from readability import Document
from dataclasses import dataclass

load_dotenv(find_dotenv())
@dataclass
class DadosPagina:
    url_original: str
    conteudo_markdown: str
    links: list
    titulo_pagina: str

class Validador:
    def __init__(self, config):
        self.extensoes_invalidas = config.get("extensoes_invalidas", [])
        self.segmentos_invalidos = config.get("segmentos_de_caminho_invalido", [])
        self.protocolos_invalidos = config.get("protocolos_invalidos", [])
        self.prefixos_permitidos = config.get("prefixos_de_caminho_permitidos", [])
        self.dominios_permitidos = config.get("dominios_permitidos", [])
    def validar_pagina(self, dados: DadosPagina) -> tuple[bool, str]:
        if any(dados.url_original.endswith(extensao) for extensao in self.extensoes_invalidas):
            return (False, "Extensão de arquivo invalida")
        
        url = dados.url_original
        pagina_de_indice = url.endswith("/") or url.endswith("index.html")

        if not pagina_de_indice:
            if len(dados.conteudo_markdown) < 150:
                return (False, "Conteúdo muito curto")
        
        titulo_lower = dados.titulo_pagina.lower()
        if '404' in titulo_lower or 'not found' in titulo_lower or 'página não encontrada' in titulo_lower or 'error' in titulo_lower:
            return (False, "Página de erro 404")
        
        conteudo_lower = dados.conteudo_markdown.lower()
        palavras_invalidas = ['faça seu login', 'carrinho de compras', 'fórum de discussão', 'comentários', 'compre', 'blog de discussões']
        if any(palavra in conteudo_lower for palavra in palavras_invalidas):
            return (False, "Página inválida, foi encontrada uma palavra inválida")
        
        return (True, "Página válida")

        # Extrair a versão da url ou do título da página
    def validar_link_novo(self, url_base: str, link_url: str) -> bool:
        url_parsed = urlparse(url_base)
        str_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path

        link_completo = urljoin(str_url, link_url)
        parsed_link = urlparse(link_completo)
        str_link = parsed_link.scheme + "://" + url_parsed.netloc + url_parsed.path

        dominio_principal = extrair_dominio_principal(str_link)
        dominio_do_link = parsed_link.hostname
        caminho_do_link = (parsed_link.path or "/").lower()

        dominios_permitidos = []

        if dominio_principal in self.dominios_permitidos:
            dominios_permitidos = self.dominios_permitidos[dominio_principal]
            print(f"INFO: Usando escopo amplo para a vizinhança conhecida: {dominio_principal}")
        else:
            dominio_exato = parsed_link.hostname
            dominios_permitidos.append(dominio_exato)
            print(f"INFO: Usando escopo restrito para o domínio: {dominio_exato}")

        if dominio_do_link not in dominios_permitidos:
            return False

        if not any(caminho_do_link.startswith(prefixo) for prefixo in self.prefixos_permitidos):
            return False

        if any(str_link.startswith(protocolo) for protocolo in self.protocolos_invalidos):
            return False

        if any(item_invalido in str_link.lower() for item_invalido in self.segmentos_invalidos):
            return False

        return True

def verificar_https(url):
    url_analisada = urlparse(url)
    if not url_analisada.scheme:
        print(f"URL '{url}' não tem esquema. Adicionando 'https://' como padrão.")
        str_link = 'https://' + url
        return str_link
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
        conteudo_html = pagina.content()
        soup = BeautifulSoup(conteudo_html, 'lxml')
        print("conteúdo da página extraído")

        documento = Document(conteudo_html)
        conteudo = documento.summary
        titulo_pagina = documento.title()

        conteudo_markdown = md(str(conteudo))
        links = []

        for elemento in soup.find_all('a', href=True):
            if isinstance(elemento, Tag):
                links.append(elemento.get("href"))

        print("convertendo o conteúdo em markdown")
        return DadosPagina(
            url_original=url,
            conteudo_markdown=conteudo_markdown,
            links=links,
            titulo_pagina=titulo_pagina
        )

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

def main(nome_colecao, url):
    print("Iniciando o processo...")
    url = verificar_https(url)
    print(url)
    config = carregar_config_urls()
    validador = Validador(config)

    urls_vistas = []
    urls_para_acessar = []
    urls_rejeitadas = []

    if not url in urls_para_acessar:
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

            urls_vistas.append(url_atual)

            dados_pagina_atual = extrair_dados_da_pagina(pagina, url_atual)

            if not dados_pagina_atual:
                print("A página não possui dados ou não foi carregada")
                continue

            valido, motivo = validador.validar_pagina(dados_pagina_atual)

            if not valido:
                print(f"A página {url_atual} é inválida pelo motivo: {motivo}")
                continue

            print("\n\nPágina aprovada!! Salvando conteúdo")

            parser = urlparse(url_atual)
            dominio = parser.hostname
            caminho = parser.path

            dominio_e_caminho = dominio + caminho
            
            nome_arquivo = "".join(["_" if caracter in "/?:-" else caracter for caracter in dominio_e_caminho ])
            conteudo_markdown = dados_pagina_atual.conteudo_markdown

            baixar_conteudo(
            nome_arquivo=nome_arquivo,
            nome_colecao=nome_colecao,
            conteudo_markdown=conteudo_markdown
            )
            print(f"\nconteúdo salvo em {nome_arquivo}")

            for link in dados_pagina_atual.links:
                url_absoluta = verificar_url_absoluto(url_atual, link)
                parsed_url = urlparse(url_absoluta)
                url_limpa = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                if url_limpa in urls_vistas or url_limpa in urls_para_acessar:
                    continue
                if verificar_url_absoluto(url_atual, link):
                    urls_para_acessar.append(url_limpa)
                else:
                    urls_rejeitadas.append(url_limpa)

    return {"urls_vistas": urls_vistas, "urls_para_acessar": urls_para_acessar, "urls_rejeitadas": urls_rejeitadas}

if __name__ == "__main__":
    tempo_inicio = time()

    pprint(main(
    nome_colecao="python_docs",
    url="https://docs.python.org/3/index.html",
    ))

    tempo_execucao = time() - tempo_inicio
    print(f"O programa levou {tempo_execucao:.2f} segundos para executar")