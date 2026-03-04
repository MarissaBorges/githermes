<!-- BADGES -->

[PYTHON_BADGE]: https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[PLAYWRIGHT_BADGE]: https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white
[BEAUTIFULSOUP_BADGE]: https://img.shields.io/badge/Beautiful%20Soup-A86454?style=for-the-badge&logo=beautifulsoup&logoColor=white
[LANGCHAIN_BADGE]: https://img.shields.io/badge/LangChain-1A1A1A?style=for-the-badge&logo=langchain&logoColor=white
[STREAMLIT_BADGE]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[RAG_BADGE]: https://img.shields.io/badge/RAG-8A2BE2?style=for-the-badge
[WIP_BADGE]: https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge

<!-- PROJECT -->
<h1 align="center" style="font-weight: bold;">GitHermes Docu-Mentor AI 🧠 (Em Desenvolvimento)</h1>

<p align="center">
  <!-- Adicione aqui os badges das tecnologias que você usou -->
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge" alt="Work in Progress Badge">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python Badge">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright Badge">
  <img src="https://img.shields.io/badge/LangChain-1A1A1A?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain Badge">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit Badge">
  <img src="https://img.shields.io/badge/RAG-8A2BE2?style=for-the-badge" alt="RAG Badge">
</p>

<p align="center">
  <a href="#-descrição">Descrição</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-destaques-técnicos">Destaques</a> •
  <a href="#-como-executar">Como Executar</a> •
  <a href="#-roadmap-futuro">Roadmap Futuro</a>
</p>

---

## 📌 Descrição

O **GitHermes Docu-Mentor AI** é um projeto para criar um assistente de IA especializado em responder perguntas sobre documentações técnicas e repositórios do GitHub. A ideia é que o usuário possa fornecer um link e, a partir dele, interagir com um chatbot para tirar dúvidas, obter exemplos de código e entender conceitos complexos.

Atualmente, o projeto está na **Fase 1: Coleta de Dados**. Foi desenvolvido um web crawler robusto e inteligente, capaz de navegar por sites de documentação, extrair o conteúdo relevante, convertê-lo para Markdown e salvá-lo localmente. Esta etapa é a base para alimentar o cérebro da futura IA.

---

## 🚀 Funcionalidades

### Funcionalidades Atuais (Web Crawler)

- **Navegação Inteligente:** Utiliza Playwright e HTTPX para navegar por sites, incluindo aqueles que dependem de JavaScript para renderizar conteúdo.
- **Extração de Conteúdo:** Emprega as bibliotecas `readability-lxml` e `BeautifulSoup` para limpar o HTML e extrair apenas o conteúdo textual principal, ignorando menus, anúncios e rodapés.
- **Conversão para Markdown:** Converte o HTML limpo para o formato Markdown, ideal para ser processado por modelos de linguagem.
- **Validação de Links e Páginas:** Possui um sistema de validação configurável (`config_urls.json`) para garantir que o crawler permaneça focado em conteúdo relevante, evitando páginas de login, fóruns ou blogs.
- **Escopo Configurável:** Permite definir o escopo da varredura, restringindo-a a subdomínios específicos ou versões de documentação.

### Funcionalidades Planejadas (Assistente RAG)

- **Interface Interativa com Streamlit:** Uma interface web amigável para o usuário inserir links e conversar com a IA.
- **Processamento de Linguagem com LangChain:** Utilização do framework LangChain para orquestrar o fluxo de **RAG (Retrieval-Augmented Generation)**.
- **Indexação e Busca Vetorial:** O conteúdo em Markdown será dividido, transformado em vetores (embeddings) e armazenado em um banco de dados vetorial para buscas semânticas rápidas.
- **Suporte a Múltiplos Modelos:** Permitirá a integração com modelos de linguagem gratuitos e a opção para o usuário inserir sua própria chave da API da OpenAI para usar modelos como o GPT-4.

---

## 🔒 Destaques Técnicos

- **Crawler Híbrido:** Combina a velocidade do `HTTPX` para requisições simples com a robustez do `Playwright` para páginas complexas, otimizando a performance da coleta.
- **Sistema de Validação Flexível:** A lógica de validação de URLs, domínios, prefixos e versões é centralizada na classe `Validador` e configurada via JSON, permitindo fácil adaptação para diferentes sites de documentação.
- **Limpeza de Conteúdo Eficaz:** O uso da biblioteca `readability` do Mozilla garante uma extração de alta qualidade do corpo principal do texto, resultando em dados mais limpos para o treinamento da IA.
- **Logging Detalhado:** O sistema registra todas as ações, decisões e erros em um arquivo de log (`crawler_log.log`), facilitando a depuração e o monitoramento do processo.

---

## 📍 Como Executar

**(Fase Atual: Crawler)**

Siga as instruções abaixo para executar o web crawler em seu ambiente local.

### Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### Clonando o Repositório

```bash
# Clone o projeto para a sua máquina local
git clone https://github.com/MarissaBorges/githermes.git

# Entre no diretório do projeto
cd githermes
```

### Instale as Dependências

É altamente recomendado criar um ambiente virtual.

```bash
# Crie e ative o ambiente virtual
python -m venv .venv

# Ativar no Windows:
.venv\Scripts\Activate
# Ativar no macOS/Linux:
source .venv/bin/activate

# Instale o projeto e suas dependências
# Opção 1: Usando pip (modo de desenvolvimento)
pip install -e .

# Opção 2: Usando uv (mais rápido)
uv sync

# O Playwright requer a instalação dos navegadores
playwright install
```

### Iniciando o Projeto

O script principal pode ser configurado e executado diretamente.

```bash
# Execute o script Python
python scraper.py
```

- Você pode alterar a URL de início, o nome da coleção e outras configurações diretamente na seção `if __name__ == "__main__":` do arquivo `scraper.py`.
- O conteúdo coletado será salvo na pasta `data/collections/`.

---

## 🗺️ Roadmap Futuro

- [ ] **Fase 2: Interface e Indexação:**
  - [ ] Desenvolver a interface básica com Streamlit.
  - [ ] Implementar a lógica de processamento de arquivos (chunking, embedding).
  - [ ] Integrar com um banco de dados vetorial (ex: FAISS, ChromaDB).
- [ ] **Fase 3: Lógica de Conversação (RAG):**
  - [ ] Construir a cadeia de conversação com LangChain.
  - [ ] Integrar com um modelo de linguagem open-source.
- [ ] **Fase 4: Recursos Avançados:**
  - [ ] Adicionar suporte para chaves de API da OpenAI.
  - [ ] Implementar cache de respostas e histórico de conversas.
  - [ ] Adicionar suporte para análise de repositórios do GitHub.

---

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MarissaBorges">
        <img src="https://github.com/MarissaBorges.png?size=100" width="100px;" alt="Foto de Marissa Borges"/><br>
        <sub>
          <b>Marissa Borges</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

## 📫 Como Contribuir

O projeto está em estágio inicial e contribuições são muito bem-vindas!

1.  Faça um **Fork** do projeto.
2.  Crie uma nova branch para sua Feature (`git checkout -b feature/AmazingFeature`).
3.  Faça o **Commit** de suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4.  Faça o **Push** da sua branch (`git push origin feature/AmazingFeature`).
5.  Abra um **Pull Request**.
