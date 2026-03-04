import threading
import psutil
import logging
from time import time
from loaders.scraper import scraper_docs

logging.basicConfig(
    filename="testando_batchs.log",
    filemode="w",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

uso_cpu = []
monitorando = True
lock_monitorando = threading.Lock()
lock_uso_cpu = threading.Lock()


def monitor_cpu():
    global monitorando, uso_cpu
    while True:
        with lock_monitorando:
            if not monitorando:
                break
        cpu = psutil.cpu_percent(interval=1)
        with lock_uso_cpu:
            uso_cpu.append(cpu)


params = {
    "nome_colecao": "streamlit-docs",
    "url": "https://docs.streamlit.io/",
    "versao": "",
    "acessar_links_internos": True,
    "batch_size": 30,
    "profundidade": 24,
}

tempo_inicio = time()

thread_cpu = threading.Thread(target=monitor_cpu)
thread_cpu.start()

logging.info(
    f"Testando o uso de batchs e monitorando a CPU. Batch={params.get('batch_size')}"
)
resultado = scraper_docs(**params)

with lock_uso_cpu:
    logging.info(f"Uso da CPU: {uso_cpu}")
with lock_monitorando:
    monitorando = False
thread_cpu.join()

tempo_execucao = time() - tempo_inicio
logging.info(f"O programa levou {tempo_execucao:.2f} segundos para executar")
print("programa finalizado")
print(f"O programa levou {tempo_execucao:.2f} segundos para executar")
with lock_uso_cpu:
    print(f"Uso de CPU durante execução: {uso_cpu}")
