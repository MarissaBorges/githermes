import requests
import zipfile
import io
import os

def download_repo(url_repo):
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

repo_url = "https://github.com/MarissaBorges/teste"
download_repo(repo_url)