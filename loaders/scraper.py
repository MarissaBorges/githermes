from playwright.async_api import async_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import os
import json
from time import time
from dotenv import load_dotenv, find_dotenv
from readability import Document
from typing import Optional
from dataclasses import dataclass
import re
from packaging import version
import logging
import httpx
from fake_useragent import UserAgent
import asyncio
from fuzzywuzzy import fuzz
from pathlib import Path

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
        self.caminhos_raiz_permitidos = config.get("caminhos_raiz_permitidos", [])
        self.segmentos_de_url_valida = config.get("segmentos_de_url_valida", [])
        self.versao = str(versao) if versao else None
        self.dominios_permitidos = config.get("dominios_permitidos", {})
        self.dominio_base = None

        self.threshold_link = config.get("pontuacao", {}).get("threshold_link", 50)
        self.threshold_pagina = config.get("pontuacao", {}).get("threshold_pagina", 50)
        
        self.pesos = config.get("pontuacao", {}).get("pesos", {
            "protocolo": 10,
            "dominio": 15,
            "prefixo": 15,
            "extensao": 10,
            "segmentos": 20,
            "versao": 15
        })
        self.penalidades = config.get("pontuacao", {}).get("penalidades", {
            "protocolo_invalido": -60,
            "dominio_invalido": -40,
            "extensao_binaria": -30,
            "segmento_proibido": -40
        })
        
        self.extensoes_invalidas_set = set(self.extensoes_invalidas)
        self.protocolos_invalidos_set = set(self.protocolos_invalidos)
        self.segmentos_invalidos_set = set(self.segmentos_invalidos)
        self.prefixos_permitidos_set = set(self.prefixos_permitidos + self.caminhos_raiz_permitidos)
        self.segmentos_de_url_valida_set = set(self.segmentos_de_url_valida)
        
        self._versao_pattern = re.compile(r'/(?:v|version/)?(\d+(?:\.\d+)?)/')
        self._protocolo_pattern = re.compile(r'^https?://')
        self._palavras_proibidas_pattern = re.compile(
            r'carrinho de compras|faça seu login|fórum de discussão|compre agora',
            re.IGNORECASE
        )
        self._doc_keywords_pattern = re.compile(
            r'documentation|docs|api reference|developer guide|manual',
            re.IGNORECASE
        )

    def _extrair_versao_da_url(self, url: str) -> Optional[str]:
        match = self._versao_pattern.search(url)
        if match:
            return match.group(1)
        return None
    
    def _definir_dominios(self, url_base):
        dominio_inicial = urlparse(url_base).hostname
        logging.info(f"Escopo restrito para o domínio: {dominio_inicial}")
        
        return dominio_inicial
    
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

    async def validar_pagina_atual(self, dados: DadosPagina) -> tuple[bool, str]:
        pontos = 0
        detalhes = []

        try:
            tamanho = len(dados.conteudo_markdown)
            titulo_lower = dados.titulo_pagina.lower()
            conteudo_lower = dados.conteudo_markdown.lower()
            
            if '404' in titulo_lower or 'not found' in titulo_lower or 'página não encontrada' in titulo_lower:
                return (False, "Página de erro 404")

            if tamanho < 100:
                return (False, f"Conteúdo insuficiente ({tamanho} chars)")
            
            if self._palavras_proibidas_pattern.search(conteudo_lower):
                pontos -= 30
                detalhes.append("-30 contém palavras proibidas")
            
            tem_estrutura = '#' in dados.conteudo_markdown or '```' in dados.conteudo_markdown
            if tem_estrutura:
                pontos += 50
                detalhes.append("+50 boa estrutura")
            else:
                pontos += 30
                detalhes.append("+30 estrutura mínima")
            
            if tamanho >= 300:
                pontos += 30
                detalhes.append("+30 conteúdo grande")
            elif tamanho >= 150:
                pontos += 15
                detalhes.append("+15 conteúdo médio")
            else:
                pontos += 5
                detalhes.append("+5 conteúdo pequeno")
            
            if '```' in dados.conteudo_markdown or '`' in dados.conteudo_markdown:
                pontos += 20
                detalhes.append("+20 contém código")
            
            valido = pontos >= self.threshold_pagina
            detalhes_str = " | ".join(detalhes)
            motivo = f"Pontuação: {pontos}/{self.threshold_pagina} ({detalhes_str})"
            
            return (valido, motivo)
        
        except Exception as e:
            logging.error(f"Erro ao validar página {dados.url_original}: {e}")
            return (False, f"Erro na validação: {str(e)}")

    async def validar_link_novo(self, url_base: str, link_url: str) -> tuple[bool, str]:
        pontos = 0
        detalhes = []

        try:
            link_completo = urljoin(url_base, link_url)
            parsed_link = urlparse(link_completo)
            dominio_do_link = parsed_link.hostname
            caminho_do_link = (parsed_link.path or "/").lower()
            str_link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path

            if not self.dominio_base:
                self.dominio_base = urlparse(url_base).hostname

            protocolo_valido = not any(link_completo.startswith(p) for p in self.protocolos_invalidos)
            if protocolo_valido:
                resultado = self.pesos.get("protocolo", 10)
                detalhes.append(f"+{self.pesos.get('protocolo', 10)} protocolo válido")
            else:
                resultado = self.penalidades.get("protocolo", -60)
                detalhes.append(f"{self.penalidades.get('protocolo', -60)} protocolo inválido")
            pontos += resultado

            lista_dominios_permitidos = set()
            if isinstance(self.dominios_permitidos, dict):
                for dominios_list in self.dominios_permitidos.values():
                    if isinstance(dominios_list, list):
                        lista_dominios_permitidos.update(dominios_list)
            
            dominio_valido = (dominio_do_link == self.dominio_base or dominio_do_link in lista_dominios_permitidos)
            if dominio_valido:
                resultado = self.pesos.get("dominio", 15)
                detalhes.append(f"+{self.pesos.get('dominio', 15)} domínio válido")
            else:
                resultado = self.penalidades.get("dominio", -40)
                detalhes.append(f"{self.pesos.get('dominio', -40)} domínio inválido ({dominio_do_link})")
            pontos += resultado

            if caminho_do_link == "/":
                resultado = self.pesos.get("prefixo", 15)
                detalhes.append(f"+{self.pesos.get('prefixo', 15)} página raiz")
            else:
                prefixo_valido = False
                for prefixo in self.prefixos_permitidos_set:
                    if caminho_do_link.startswith(f"/{prefixo}/") or caminho_do_link == f"/{prefixo}":
                        prefixo_valido = True
                        break
                
                if prefixo_valido:
                    resultado = self.pesos.get("prefixo", 15)
                    detalhes.append(f"+{self.pesos.get('prefixo', 15)} prefixo válido")
                else:
                    razao_fuzzy = max(
                        [fuzz.ratio(caminho_do_link, f"/{p}/") for p in self.prefixos_permitidos] + [0]
                    )
                    if razao_fuzzy >= 75:
                        pts_fuzzy = int(self.pesos.get("prefixo", 15) * 0.8)
                        resultado = pts_fuzzy
                        detalhes.append(f"+{pts_fuzzy} prefixo similar ({razao_fuzzy}%)")
                    else:
                        detalhes.append(f"+0 prefixo desconhecido")
            pontos += resultado
        
            caminho_sem_barra = caminho_do_link.rstrip('/')
            if '.' in caminho_sem_barra.split('/')[-1]:
                if any(caminho_sem_barra.endswith(ext) for ext in self.extensoes_invalidas_set):
                    resultado = self.penalidades.get("extensao", -30)
                    detalhes.append(f"{self.penalidades.get('extensao', -30)} extensão binária")
                else:
                    resultado = self.pesos.get("extensao", 10)
                    detalhes.append(f"+{self.pesos.get('extensao', 10)} extensão válida")
            else:
                resultado = self.pesos.get("extensao", 10)
                detalhes.append(f"+{self.pesos.get('extensao', 10)} HTML válido")
            pontos += resultado

            segmento_invalido = any(seg in caminho_do_link.lower() for seg in self.segmentos_invalidos_set)
            if segmento_invalido:
                resultado = self.penalidades.get("segmentos", -50)
                detalhes.append(f"{self.penalidades.get('segmentos', -50)} segmento proibido")
            else:
                resultado = self.pesos.get("segmentos", 20)
                detalhes.append(f"+{self.pesos.get('segmentos', 20)} sem segmentos proibidos")
            pontos += resultado
        
            if self.versao:
                versao_encontrada = self._extrair_versao_da_url(link_url)
                if versao_encontrada:
                    try:
                        v_desejada = version.parse(self.versao)
                        v_encontrada = version.parse(versao_encontrada)
                        if v_encontrada.major == v_desejada.major:
                            pontos += self.pesos.get("versao", 15)
                            detalhes.append(f"+{self.pesos.get('versao', 15)} versão compatível")
                        else:
                            detalhes.append(f"+0 versão diferente ({v_encontrada.major} vs {v_desejada.major})")
                    except Exception as e:
                        logging.debug(f"Erro ao validar versão: {e}")

            valido = pontos >= self.threshold_link
            detalhes_str = " | ".join(detalhes)
            motivo = f"Pontuação: {pontos}/{self.threshold_link} ({detalhes_str})"
            
            return (valido, motivo)
        
        except Exception as e:
            logging.error(f"Erro ao validar link {link_url}: {e}")
            return (False, f"Erro na validação: {str(e)}")

    async def validar_url_inicial(self, url, user_agent):
        parsed_url = urlparse(url)
        hostname  = parsed_url.hostname
        path = parsed_url.path

        primeiro_segmento_host = hostname.split('.')[0]
        if primeiro_segmento_host in self.segmentos_de_url_valida_set:
            return (True, f"URL aprovada pelo subdomínio '{primeiro_segmento_host}'.")
        
        if path.startswith(tuple(f'/{segmento}/' for segmento in self.segmentos_de_url_valida)):
            return (True, "URL aprovada pelo prefixo do caminho.")
        
        try:
            html = await fazer_request(url, user_agent)
            soup = BeautifulSoup(html, 'lxml')
        except Exception as e:
            return (False, f"Não foi possível buscar a URL inicial para validação: {e}")

        pontuacao = []
        
        titulo = soup.title.string.lower() if soup.title and soup.title.string else ''
        if self._doc_keywords_pattern.search(titulo):
            pontuacao.append(True)

        h1 = soup.h1.string.lower() if soup.h1 and soup.h1.string else ''
        if self._doc_keywords_pattern.search(h1):
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

class GerenciarJson():
    def __init__(self, caminho_colecao=None):
        self.caminho_colecao = caminho_colecao
        self.dados_cache = {}
        self._carregado = False
    
    def _garantir_carregado(self, nome_colecao=None):
        if nome_colecao and not self._carregado:
            caminho = f"data/collections/{nome_colecao}"
            caminho_json = f"{caminho}/urls.json"
            try:
                if os.path.exists(caminho_json):
                    with open(caminho_json, "r", encoding="utf-8") as f:
                        self.dados_cache = json.load(f)
                else:
                    self.dados_cache = {}
            except Exception as e:
                logging.error(f"Erro ao ler o arquivo JSON: {e}")
                self.dados_cache = {}
            self._carregado = True
    
    def adicionar_no_json(self, nome_colecao, url, tipo_url):
        self._garantir_carregado(nome_colecao)
        
        if tipo_url not in self.dados_cache:
            self.dados_cache[tipo_url] = []
        
        if url not in self.dados_cache[tipo_url]:
            self.dados_cache[tipo_url].append(url)
    
    def salvar_json(self, nome_colecao):
        caminho = f"data/collections/{nome_colecao}"
        caminho_json = f"{caminho}/urls.json"
        
        os.makedirs(caminho, exist_ok=True)
        
        try:
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(self.dados_cache, f, ensure_ascii=False, indent=2)
            logging.info(f"JSON salvo com sucesso em {caminho_json}")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo JSON: {e}")

    def carregar_json(self, caminho_do_arquivo="config_urls.json"):
        try:
            with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}            
        except json.JSONDecodeError:
            logging.error(f"ERRO: O arquivo '{caminho_do_arquivo}' tem um erro de sintaxe JSON.")
        return {}

def verificar_protocolo_https(url):
    url_analisada = urlparse(url)
    if not url_analisada.scheme:
        logging.info(f"URL '{url}' não tem esquema. Adicionando 'https://' como padrão.")
        str_link = 'https://' + url
        return str_link
    return url

def verificar_url_completa(url_base, url):
    url_absoluta = urljoin(url_base, url)
    return url_absoluta

async def fazer_request(url, user_agent):
    headers = {'User-Agent': user_agent}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(url, timeout=10.0)
    if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
        return response.text
    else:
        raise ValueError("Resposta não-HTML ou com erro")

async def obter_varios_conteudos_html(urls, pagina_playwright, user_agent):
    tasks = [fazer_request(url, user_agent) for url in urls]
    resultados = list(await asyncio.gather(*tasks, return_exceptions=True))
    for i, resultado in enumerate(resultados):
        if isinstance(resultado, Exception) or not resultado:
            try:
                await pagina_playwright.goto(urls[i], wait_until="domcontentloaded", timeout=15000)
                resultados[i] = await pagina_playwright.content()
            except Exception:
                resultados[i] = Exception("Falha ao obter conteúdo com httpx e Playwright")
                logging.error(f"Erro Playwright: {urls[i]}")
    return resultados

def converter_html_para_markdown(conteudo_html, url):
    soup = BeautifulSoup(conteudo_html, 'lxml')
    documento = Document(conteudo_html)
    html_limpo = documento.summary()
    titulo_pagina = documento.title()
    conteudo_markdown = md(str(html_limpo))
    
    links = []
    for elemento in soup.find_all('a', href=True):
        if isinstance(elemento, Tag):
            href = elemento.attrs.get("href")
            if href:
                links.append(href)

    return DadosPagina(
        url_original=url,
        conteudo_markdown=conteudo_markdown,
        links=links,
        titulo_pagina=titulo_pagina
    )

def baixar_conteudo(nome_colecao, nome_arquivo, conteudo_markdown):
    try:
        caminho_colecao = f"data/collections/{nome_colecao}"
        os.makedirs(caminho_colecao, exist_ok=True)
        with open(f"{caminho_colecao}/{nome_arquivo}.md", 'w', encoding="utf-8") as file:
            file.write(conteudo_markdown)
        logging.info(f"Página salva: {nome_arquivo}")
    except (OSError, IOError, TypeError) as e:
        logging.error(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

async def main(nome_colecao, url, versao=None, acessar_links_internos=True, batch_size = 5, profundidade=1):
    logging.info("Iniciando o processo...")

    ua = UserAgent(browsers='Chrome', platforms='desktop')
    user_agent = ua.random

    url = verificar_protocolo_https(url)
    logging.info(url)
    
    gerenciar_json = GerenciarJson(nome_colecao)
    config = gerenciar_json.carregar_json("config_urls.json")
    validador = Validador(config, versao)

    url_valida, msg_valida = await validador.validar_url_inicial(url, user_agent)
    if url_valida:
        json_urls_vistas = gerenciar_json.carregar_json(f"data/collections/{nome_colecao}/urls.json")
        json_urls_vistas_set = set(json_urls_vistas.get("urls_vistas", []))
        urls_vistas = set()
        urls_para_acessar = [url]
        urls_rejeitadas = []
        paginas_salvas_contador = 0

        gerenciar_json.adicionar_no_json(nome_colecao, url, "urls_vistas")

        async with async_playwright() as pw:
            navegador = await pw.chromium.launch(headless=True)
            pagina_playwright = await navegador.new_page()
            logging.info("Playwright inicializado com sucesso")

            while paginas_salvas_contador < profundidade and urls_para_acessar:
                batch = []
                while urls_para_acessar and len(batch) < batch_size:
                    url_atual = urls_para_acessar.pop(0)
                    if url_atual in urls_vistas:
                        continue
                    batch.append(url_atual)
                    urls_vistas.add(url_atual)

                if not batch:
                    logging.info("Nenhuma URL válida para processar no batch. Encerrando.")
                    break

                conteudos_html = await obter_varios_conteudos_html(batch, pagina_playwright=pagina_playwright, user_agent=user_agent)

                for url_atual, conteudo_html_atual in zip(batch, conteudos_html):
                    if paginas_salvas_contador >= profundidade:
                        break
                    if isinstance(conteudo_html_atual, Exception) or not conteudo_html_atual:
                        logging.error(f"Erro ao obter {url_atual}: {conteudo_html_atual}")
                        continue

                    dados_pagina_atual = converter_html_para_markdown(conteudo_html_atual, url_atual)

                    if not dados_pagina_atual:
                        logging.error("A página não possui dados ou não foi carregada")
                        continue

                    if acessar_links_internos:
                        pagina_valida, pagina_motivo = await validador.validar_pagina_atual(dados_pagina_atual)

                        logging.info(f"Processando {len(dados_pagina_atual.links)} novos links")
                        for link in dados_pagina_atual.links:
                            if not link:
                                logging.info(f"Link vazio ignorado na página {url_atual}")
                                continue

                            parsed_url = urlparse(verificar_url_completa(url_atual, link))
                            url_limpa = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

                            if url_limpa.startswith('http://'):
                                url_limpa = 'https' + url_limpa[4:]

                            if url_limpa == 'https://':
                                logging.info(f"Link ignorado: {url_limpa} (apenas esquema)")
                                continue

                            if url_limpa in urls_vistas or url_limpa in urls_para_acessar or url_limpa in urls_rejeitadas or url_limpa in json_urls_vistas_set:
                                logging.info(f"Link já processado ou na fila: {url_limpa}")
                                continue

                            link_valido, link_motivo = await validador.validar_link_novo(
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

                    gerenciar_json.adicionar_no_json(nome_colecao, url_atual, "urls_vistas")
                    baixar_conteudo(
                        nome_arquivo=nome_arquivo,
                        nome_colecao=nome_colecao,
                        conteudo_markdown=conteudo_markdown
                    )
                    if not profundidade == 1:
                        paginas_salvas_contador += 1
                    logging.info(f"conteúdo salvo em {nome_arquivo}")

            gerenciar_json.salvar_json(nome_colecao)
            await navegador.close()

        return {"urls_vistas": list(urls_vistas), "urls_para_acessar": urls_para_acessar, "urls_rejeitadas": urls_rejeitadas}
    
    return f"URL não parece ser de uma documentação: {msg_valida}"

def scraper_docs(**params):
    logging.info(f"Iniciando o scraper com os seguintes parâmetros: {json.dumps(params, indent=4)}")

    resultado = asyncio.run(main(**params))
    return resultado

if __name__ == "__main__":
    logging.basicConfig(
        filename="crawler_log.log",
        filemode="w",
        level=logging.INFO,
        encoding="utf-8",
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    tempo_inicio = time()

    params = {
        "nome_colecao": "python-docs",
        "url": "https://docs.python.org/3/",
        "versao": 3.11,
        "acessar_links_internos": True,
        "batch_size": 30,
        "profundidade": 200
    }
    logging.info(f"Técnica de Gerenciamento de urls com json implementada")
    logging.info(f"Iniciando o scraper com os seguintes parâmetros: {json.dumps(params, indent=4)}")

    resultado = scraper_docs(**params)

    logging.info(resultado)

    tempo_execucao = time() - tempo_inicio
    logging.info(f"O programa levou {tempo_execucao:.2f} segundos para executar")
    print(f"\n✅ Concluído em {tempo_execucao:.2f}s")
    
    if isinstance(resultado, dict):
        print(f"  URLs vistas: {len(resultado.get('urls_vistas', []))}")
        print(f"  URLs para acessar: {len(resultado.get('urls_para_acessar', []))}")
        print(f"  URLs rejeitadas: {len(resultado.get('urls_rejeitadas', []))}")
    else:
        print(resultado)