from playwright.sync_api import sync_playwright, Error, TimeoutError
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import os
from pprint import pprint
import json
import tldextract
from time import time, sleep
from dotenv import load_dotenv, find_dotenv
from readability import Document
from typing import Optional
from dataclasses import dataclass
import re
from packaging import version
import logging
import httpx
from fake_useragent import UserAgent

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
        self.prefixos_permitidos = config.get("prefixos_permitidos", [])
        self.dominios_permitidos = config.get("dominios_permitidos", [])
        self.caminhos_raiz_permitidos = config.get("caminhos_raiz_permitidos", [])
        self.versao = versao

    def _extrair_versao_da_url(self, url: str) -> Optional[str]:
        padrao = r'/(?:v|version/)?(\d+(?:\.\d+)?)/'
        match = re.search(padrao, url)
        if match:
            return match.group(1)
        return None
    
    def _definir_dominios(self, url_base):
        dominio_principal_atual = extrair_dominio_principal(url_base)
        dominios_permitidos = []

        dominios_conhecidos_json = self.dominios_permitidos

        if dominio_principal_atual in dominios_conhecidos_json:
            dominios_permitidos.append(dominios_conhecidos_json[dominio_principal_atual])
            logging.info(f"Escopo amplo ativado para a dominios conhecidos: {dominios_permitidos}")
        else:
            dominio_inicial = urlparse(url_base).hostname
            dominios_permitidos.append(dominio_inicial)
            logging.info(f"Escopo restrito para o domínio: {dominios_permitidos}")
        
        return dominios_permitidos
    
    def _validar_versao_da_url(self, versao_solicitada: str, versao_encontrada: str):
        try:
            v_desejada = version.parse(versao_solicitada)
        except version.InvalidVersion:
            return (False, f"Versão desejada '{versao_solicitada}' é inválida.")

        if versao_encontrada is None:
            return (True, "Nenhuma versão encontrada na URL, permitido como genérico.")

        try:
            v_encontrada = version.parse(versao_encontrada)
        except version.InvalidVersion:
            return (False, f"Versão encontrada '{versao_encontrada}' é inválida.")

        if v_encontrada.major != v_desejada.major:
            return (False, f"Major incorreto. Esperado: {v_desejada.major}, encontrado: {v_encontrada.major}")

        if len(v_encontrada.release) == 1:
            return (True, f"Versão genérica major '{v_encontrada.major}' permitida.")

        if v_encontrada.minor != v_desejada.minor:
            return (False, f"Minor incorreto. Esperado: {v_desejada.minor}, encontrado: {v_encontrada.minor}")

        return (True, f"Versão '{v_encontrada}' compatível.")

    def validar_pagina(self, dados: DadosPagina) -> tuple[bool, str]:
        url = dados.url_original
        pagina_de_indice = url.endswith("/") or url.endswith("index.html") or url.endswith("contents.html")

        if not pagina_de_indice and len(dados.conteudo_markdown) < 150:
            return (False, "Conteúdo muito curto")
        
        titulo_lower = dados.titulo_pagina.lower()
        if '404' in titulo_lower or 'not found' in titulo_lower or 'página não encontrada' in titulo_lower or 'error' in titulo_lower:
            return (False, "Página de erro 404")
        
        conteudo_lower = dados.conteudo_markdown.lower()
        palavras_invalidas = ['faça seu login', 'carrinho de compras', 'fórum de discussão', 'comentários', 'compre', 'blog de discussões']
        if any(palavra in conteudo_lower for palavra in palavras_invalidas):
            return (False, "Página inválida, foi encontrada uma palavra inválida")
        
        return (True, "Página válida")

    def validar_link_novo(self, url_base: str, link_url: str) -> tuple[bool, str]:
        link_completo = urljoin(url_base, link_url)
        parsed_link = urlparse(link_completo)
        str_link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path

        if any(str_link.startswith(protocolo) for protocolo in self.protocolos_invalidos):
            return (False, f"Protocolo inválido, link: {str_link}")

        dominios_permitidos = self._definir_dominios(url_base)
        dominio_do_link = parsed_link.hostname
        if dominio_do_link not in dominios_permitidos[0]:
            return (False, f"Domínio inválido, domínio: {dominio_do_link}")

        caminho_do_link = (parsed_link.path or "/").lower()
        if caminho_do_link == "/":
            return (True, "Link aprovado (página inicial)")
        logging.info(f"Caminho do link: {caminho_do_link}")

        prefixo_valido = False
        if self.versao:
            major_version = str(version.parse(self.versao).major)
            prefixo_valido = any(
                caminho_do_link.startswith(f"/{major_version}/{prefixo_base}/")
                for prefixo_base in self.prefixos_permitidos
            )
        
        caminho_raiz_valido = any(
            caminho_do_link.startswith(f"/{prefixo}/") or caminho_do_link == f"/{prefixo}"
            for prefixo in self.caminhos_raiz_permitidos
        )
        if not (prefixo_valido or caminho_raiz_valido):
            return (False, f"Prefixo inválido, caminho do link: {caminho_do_link}")
        
        if any(link_url.endswith(extensao) for extensao in self.extensoes_invalidas):
            return (False, "Extensão de arquivo invalida")

        if any(item_invalido in caminho_do_link.lower() for item_invalido in self.segmentos_invalidos):
            return (False, f"Segmento inválido, link: {str_link}")
        
        if self.versao:
            versao_encontrada = self._extrair_versao_da_url(link_url)
            if versao_encontrada:
                validacao, msg = self._validar_versao_da_url(self.versao, versao_encontrada)
                if not validacao:
                    return False, msg

        return (True, "Link aprovado")

def validar_url_inicial(url, user_agent):
    parsed_url = urlparse(url)
    hostname  = parsed_url.hostname
    path = parsed_url.path

    segmentos_de_url_valida = ['docs', 'documentation', 'dev', 'developer', 'api', 'guide', 'help', 'support']

    primeiro_segmento_host = hostname.split('.')[0]
    if primeiro_segmento_host in segmentos_de_url_valida:
        return (True, f"URL aprovada pelo subdomínio '{primeiro_segmento_host}'.")
    
    if path.startswith(tuple(f'/{sinal}/' for sinal in segmentos_de_url_valida)):
        return (True, "URL aprovada pelo prefixo do caminho.")
    
    try:
        html = fazer_request(url, user_agent)
        soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        return (False, f"Não foi possível buscar a URL inicial para validação: {e}")

    pontuacao = []
    
    titulo = soup.title.string.lower() if soup.title and soup.title.string else ''
    if any(sinal in titulo for sinal in ['documentation', 'docs', 'api reference', 'developer guide', 'manual']):
        pontuacao.append(True)

    h1 = soup.h1.string.lower() if soup.h1 and soup.h1.string else ''
    if any(sinal in h1 for sinal in ['documentation', 'api', 'guide']):
        pontuacao.append(True)

    if soup.find('pre'):
        pontuacao.append(True)
        
    texto_pagina = soup.get_text().lower()
    if not any(sinal in texto_pagina for sinal in ['carrinho de compras', 'fórum', 'blog', 'loja', 'preços']):
        pontuacao.append(True)

    if pontuacao.count(True) >= 2:
        return (True, f"URL aprovada pela análise de conteúdo")
    else:
        return (False, f"URL rejeitada. Não é uma documentação")

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

def fazer_request(url, user_agent):
    headers = {'User-Agent': user_agent}

    with httpx.Client(headers=headers, follow_redirects=True) as client:
        response = client.get(url, timeout=10.0)
    
    if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
        conteudo_html = response.text
        logging.info(f"Página {url} obtida usando httpx")
    else:
        raise ValueError("Resposta não-HTML ou com erro")
    return conteudo_html

def obter_conteudo_html(url, pagina_playwright, user_agent):
    try:
        return fazer_request(url, user_agent)
    except Exception as e:
        logging.warning(f"Falha ao usar HTTPX para {url} ({e}). Usando Playwright.")
        try:
            pagina_playwright.goto(url, wait_until="domcontentloaded", timeout=15000)
            return pagina_playwright.content()
        except Exception as playwright_error:
            logging.error(f"Falha do Playwright ao acessar {url}: {playwright_error}")
            return None

def converter_html_para_markdown(conteudo_html, url):
    if not conteudo_html:
        return None
    
    soup = BeautifulSoup(conteudo_html, 'lxml')
    logging.info("conteúdo da página extraído")

    documento = Document(conteudo_html)
    html_limpo = documento.summary()
    titulo_pagina = documento.title()

    conteudo_markdown = md(str(html_limpo))
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

def baixar_conteudo(nome_colecao, nome_arquivo, conteudo_markdown):
    try:
        caminho_colecao = f"data/collections/{nome_colecao}"
        logging.info(f"Baixando conteúdo no caminho: {caminho_colecao}")
        os.makedirs(caminho_colecao, exist_ok=True)
        with open(f"{caminho_colecao}/{nome_arquivo}.md", 'w', encoding="utf-8") as file:
            file.write(conteudo_markdown)
            logging.info(f"Conteúdo da página salvo com sucesso. Arquivo: {nome_arquivo}.md")
    except (OSError, IOError, TypeError) as e:
        logging.error(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

def main(nome_colecao, url, versao=None):
    logging.info("Iniciando o processo...")

    ua = UserAgent(browsers='Chrome', platforms='desktop')
    user_agent = ua.random

    url_valida = validar_url_inicial(url, user_agent)
    if url_valida:
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
            pagina_playwright = navegador.new_page()
            logging.info("Playwright inicializado com sucesso")

            while urls_para_acessar:
                url_atual = urls_para_acessar.pop(0)

                if url_atual in urls_vistas:
                    continue

                logging.info(f"Verificando a url: {url_atual}")

                urls_vistas.append(url_atual)

                conteudo_html_atual = obter_conteudo_html(url_atual, pagina_playwright, user_agent)

                dados_pagina_atual = converter_html_para_markdown(conteudo_html_atual, url_atual)

                if not dados_pagina_atual:
                    logging.error("A página não possui dados ou não foi carregada")
                    continue

                pagina_valida, pagina_motivo = validador.validar_pagina(dados_pagina_atual)

                logging.info(f"Processando {len(dados_pagina_atual.links)} novos links")
                for link in dados_pagina_atual.links:
                    if not link:
                        continue

                    url_absoluta = verificar_url_absoluto(url_atual, link)

                    parsed_url = urlparse(url_absoluta)
                    url_limpa = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

                    if url_limpa.startswith('http://'):
                        url_limpa = 'https' + url_limpa[4:]

                    if url_limpa in urls_vistas or url_limpa in urls_para_acessar or url_limpa in urls_rejeitadas:
                        continue
                    
                    link_valido, link_motivo = validador.validar_link_novo(
                        url_base=url_atual, 
                        link_url=url_limpa, 
                    )

                    if link_valido:
                        logging.info(f"Link APROVADO para a fila: {url_limpa}")
                        urls_para_acessar.append(url_limpa)
                    else:
                        logging.error(f"Link REJEITADO: {url_limpa}, motivo: {link_motivo}")
                        urls_rejeitadas.append(url_limpa)

                if not pagina_valida:
                    logging.info(f"A página {url_atual} é inválida pelo motivo: {pagina_motivo}")
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

        return {"urls_vistas": urls_vistas, "urls_para_acessar": urls_para_acessar, "urls_rejeitadas": urls_rejeitadas}
    
    return "URL não parece ser de uma documentação"

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
    nome_colecao="streamlit-docs",
    url="https://docs.streamlit.io/",
    # versao=""
    ))

    tempo_execucao = time() - tempo_inicio
    logging.info(f"O programa levou {tempo_execucao:.2f} segundos para executar")