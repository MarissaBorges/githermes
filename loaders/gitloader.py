import requests
from requests.exceptions import HTTPError
import zipfile
import io
import os

def validar_url(url_repo):
    try:
        resposta = requests.get(url_repo)
        resposta.raise_for_status()
        print(resposta.status_code)
        return (True, "URl válida")
    except HTTPError as httperror:
        print(f"Repositório não encontrado: {httperror}")
        return (False, httperror)
    except Exception as e:
        print(f"Ocorreu um erro ao acessar a url: {e}")
        return (False, f"URL invalida: {e}")

def download_repo(url_repo):
    url_valida = validar_url(url_repo)
    valida, motivo = url_valida
    if valida:
        url_split = url_repo.split("/")
        repositorio = url_split[-1]
        username = url_split[-2]
        zip_url = f"https://github.com/{username}/{repositorio}/archive/refs/heads/main.zip"

        caminho_destino = f"data/repos/{repositorio}"
        os.makedirs(caminho_destino, exist_ok=True)

        try:
            resposta = requests.get(zip_url)
            resposta.raise_for_status()

            with zipfile.ZipFile(io.BytesIO(resposta.content)) as zfile:
                zfile.extractall(caminho_destino)

            print(f"repositório baixado com sucesso em: {caminho_destino}")
        except Exception as e:
            print(f"ocorreu um erro na aplicação, erro: {e}")
    else:
        print(f"A URL é inválida, motivo: {motivo}")
        print(f"Por favor forneça uma url válida")

if __name__ == "__main__":
    repo_url = "https://github.com/MarissaBorges/teste"
    download_repo(repo_url)