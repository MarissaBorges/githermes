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
from typing import Optional
from dataclasses import dataclass
import re
from packaging import version
import logging

load_dotenv(find_dotenv())
@dataclass
class DadosPagina:
    url_original: str
    conteudo_markdown: str
    links: list
    titulo_pagina: str

class Validador:
    def __init__(self, config, versao):
        self.extensoes_invalidas = config.get("extensoes_invalidas", [])
        self.segmentos_invalidos = config.get("segmentos_de_caminho_invalidos", [])
        self.protocolos_invalidos = config.get("protocolos_invalidos", [])
        self.prefixos_permitidos = config.get("prefixos_de_caminho_permitidos", [])
        self.dominios_permitidos = config.get("dominios_permitidos", [])
        self.versao = versao

    def _extrair_versao_da_url(self, url: str) -> Optional[str]:
        padrao = r'/(?:v|version/)?(\d+(?:\.\d+)?)/'
        match = re.search(padrao, url)
        if match:
            return match.group(1)
        return None
    
    def _validar_versao_da_url(self, versao_solicitada: str, versao_encontrada: str):
        try:
            v_desejada = version.parse(versao_solicitada)
        except version.InvalidVersion:
            return (False, f"Versão desejada '{versao_solicitada}' é inválida.")

        if versao_encontrada is None:
            return (True, "Versão não encontrada na URL, permitido.")

        try:
            v_encontrada = version.parse(versao_encontrada)
        except version.InvalidVersion:
            return (False, f"Versão encontrada na URL '{versao_encontrada}' é inválida.")

        if v_encontrada.major != v_desejada.major:
            return (False, f"Major version incorreta. Desejada: {v_desejada.major}, Encontrada: {v_encontrada.major}")

        if v_encontrada.release == (v_encontrada.major,):
            return (True, f"Versão genérica '{v_encontrada}' permitida.")

        if v_encontrada < v_desejada:
            return (False, f"Versão encontrada '{v_encontrada}' é menor que a desejada '{v_desejada}'.")
        
        if v_encontrada > v_desejada:
            return (False, f"Versão encontrada '{v_encontrada}' é maior que a desejada '{v_desejada}'.")

        return (True, f"Versão '{v_encontrada}' compatível.")

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
        
        versao_encontrada = self._extrair_versao_da_url(dados.url_original)
        if versao_encontrada:
            validacao, msg = self._validar_versao_da_url(self.versao, versao_encontrada)
            if not validacao:
                return False, msg

        return (True, "Página válida")

    def validar_link_novo(self, url_base: str, link_url: str, dominios_permitidos: list) -> bool:
        url_parsed = urlparse(url_base)
        str_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path

        link_completo = urljoin(str_url, link_url)
        parsed_link = urlparse(link_completo)
        str_link = parsed_link.scheme + "://" + url_parsed.netloc + url_parsed.path

        dominio_do_link = parsed_link.hostname
        if dominio_do_link not in dominios_permitidos:
            return False

        caminho_do_link = (parsed_link.path or "/").lower()
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
        logging.info(f"URL '{url}' não tem esquema. Adicionando 'https://' como padrão.")
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
        logging.error(f"ERRO: Arquivo de configuração '{caminho_do_arquivo}' não encontrado.")
    except json.JSONDecodeError:
        logging.error(f"ERRO: O arquivo '{caminho_do_arquivo}' tem um erro de sintaxe JSON.")
    return {}

def extrair_dominio_principal(url_completa):
    partes_extraidas = tldextract.extract(url_completa)
    return partes_extraidas.top_domain_under_public_suffix

def extrair_dados_da_pagina(pagina, url):
    try:
        pagina.goto(url, wait_until="domcontentloaded", timeout=15000)
        conteudo_html = pagina.content()
        soup = BeautifulSoup(conteudo_html, 'lxml')
        logging.info("conteúdo da página extraído")

        documento = Document(conteudo_html)
        conteudo = documento.summary
        titulo_pagina = documento.title()

        conteudo_markdown = md(str(conteudo))
        links = []

        for elemento in soup.find_all('a', href=True):
            if isinstance(elemento, Tag):
                links.append(elemento.get("href"))

        logging.info("convertendo o conteúdo em markdown")
        return DadosPagina(
            url_original=url,
            conteudo_markdown=conteudo_markdown,
            links=links,
            titulo_pagina=titulo_pagina
        )

    except TimeoutError as e:
        logging.error(f"FALHA ESPECÍFICA: Timeout ao acessar {url}. {e}")
        return "TimeoutError"
    except Error as e:
        logging.error(f"Ocorreu um erro de Playwright/Rede ao acessar {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Ocorreu um erro ao acessar a página: {e}")
        return None

def baixar_conteudo(nome_colecao, nome_arquivo, conteudo_markdown):
    try:
        caminho_colecao = f"data/collections/{nome_colecao}"
        logging.info(f"Baixando conteúdo no caminho: {caminho_colecao}")
        os.makedirs(caminho_colecao, exist_ok=True)
        with open(f"{caminho_colecao}/{nome_arquivo}.md", 'w', encoding="utf-8") as file:
            file.write(conteudo_markdown)
            logging.info(f"Conteúdo da página salvo com sucesso. Caminho: {caminho_colecao}/{nome_arquivo}.md")
    except (OSError, IOError, TypeError) as e:
        logging.error(f"ERRO CRÍTICO ao salvar o arquivo {nome_arquivo}: {e}")

def main(nome_colecao, url, versao):
    logging.info("Iniciando o processo...")
    url = verificar_https(url)
    logging.info(url)
    config = carregar_config_urls()
    validador = Validador(config, versao)

    urls_vistas = []
    urls_para_acessar = []
    urls_rejeitadas = []

    if not url in urls_para_acessar:
        urls_para_acessar.append(url)

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)
        pagina = navegador.new_page()
        logging.info("pagina criada")

        dominio_principal_atual = extrair_dominio_principal(url)
        dominios_permitidos = []

        dominios_conhecidos_json = config.get("dominios_permitidos", [])

        if dominio_principal_atual in dominios_conhecidos_json:
            dominios_permitidos.append(dominios_conhecidos_json[dominio_principal_atual])
            logging.info(f"Escopo amplo ativado para a dominios conhecidos: {dominios_permitidos}")
        else:
            dominio_inicial = urlparse(url).hostname
            dominios_permitidos.append(dominio_inicial)
            logging.info(f"Escopo restrito para o domínio: {dominios_permitidos}")

        while urls_para_acessar:
            url_atual = urls_para_acessar.pop(0)

            if url_atual in urls_vistas:
                continue

            logging.info(f"Verificando a url: {url_atual}")

            urls_vistas.append(url_atual)

            dados_pagina_atual = extrair_dados_da_pagina(pagina, url_atual)

            if not dados_pagina_atual:
                logging.error("A página não possui dados ou não foi carregada")
                continue

            valido, motivo = validador.validar_pagina(dados_pagina_atual)

            if not valido:
                logging.info(f"A página {url_atual} é inválida pelo motivo: {motivo}")
                continue

            logging.info("Página aprovada!! Salvando conteúdo")

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
            logging.info(f"conteúdo salvo em {nome_arquivo}")

            logging.info(f"Processando{len(dados_pagina_atual.links)} novos links")
            for link in dados_pagina_atual.links:
                if not link:
                    continue

                url_absoluta = verificar_url_absoluto(url_atual, link)

                parsed_url = urlparse(url_absoluta)
                url_limpa = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

                if url_limpa in urls_vistas or url_limpa in urls_para_acessar:
                    continue

                if validador.validar_link_novo(url_atual, url_limpa, dominios_permitidos):
                    logging.info(f"Link APROVADO para a fila: {url_limpa}")
                    urls_para_acessar.append(url_limpa)
                else:
                    logging.error(f"Link REJEITADO: {url_limpa}")
                    urls_rejeitadas.append(url_limpa)

    return {"urls_vistas": urls_vistas, "urls_para_acessar": urls_para_acessar, "urls_rejeitadas": urls_rejeitadas}

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("crawler_log.log", mode='w'),
            logging.StreamHandler()
        ]
    )
    tempo_inicio = time()

    logging.info(main(
    nome_colecao="python_docs",
    url="https://docs.python.org/3/index.html",
    versao="3.11"
    ))

    tempo_execucao = time() - tempo_inicio
    logging.info(f"O programa levou {tempo_execucao:.2f} segundos para executar")