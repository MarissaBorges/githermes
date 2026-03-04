from loaders.scraper import scraper_docs
import logging
from time import time


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def main():
    """
    Entry point principal do GitHermes.
    
    Executa o web crawler com parâmetros padrão.
    Você pode modificar os parâmetros abaixo conforme necessário.
    """
    params = {
        "nome_colecao": "documentacao",
        "url": "https://example.com/docs",
        "versao": "",
        "acessar_links_internos": True,
        "batch_size": 50,
        "profundidade": 10
    }
    
    print("Iniciando o GitHermes Web Crawler...")
    tempo_inicio = time()
    
    try:
        resultado = scraper_docs(**params)
        print(resultado)
    except Exception as e:
        logging.error(f"Erro ao executar o crawler: {e}")
        print(f"Erro ao executar o crawler: {e}")
    
    tempo_execucao = time() - tempo_inicio
    print(f"Tempo total de execução: {tempo_execucao:.2f} segundos")


if __name__ == "__main__":
    main()
