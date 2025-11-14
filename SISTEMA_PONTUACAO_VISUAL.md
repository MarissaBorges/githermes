# 🎯 Sistema de Pontuação - Guia Visual

## Fluxo de Validação de Link

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VALIDAÇÃO DE LINK                           │
└─────────────────────────────────────────────────────────────────────┘

    URL: https://docs.python.org/3/library/functions.html
              ↓
    ┌─────────────────────────────────────────────────────┐
    │ 1. VERIFICAR PROTOCOLO                              │
    │    ✓ https valido? SIM → +25 pontos                │
    │    ✗ mailto:, javascript:? → REJEITA (bloqueio)    │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 2. VERIFICAR DOMÍNIO                                │
    │    ✓ docs.python.org está na whitelist? SIM → +25  │
    │    ✗ google.com? → REJEITA (bloqueio)              │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 3. VERIFICAR PREFIXO/CAMINHO                        │
    │    ✓ /3/library/ é válido? SIM → +20               │
    │    ⚠ /3/tutoriales/ (fuzzy ~90% similar) → +16    │
    │    ✗ /3/invalid/path? → 0 pontos                   │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 4. VERIFICAR EXTENSÃO                              │
    │    ✓ .html é OK? SIM → +15                         │
    │    ✗ .zip, .exe, .png? → REJEITA (bloqueio)        │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 5. VERIFICAR SEGMENTOS                              │
    │    ✓ Sem /search, /login, /cart? SIM → +15         │
    │    ✗ Contém bloqueado? → REJEITA (bloqueio)        │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 6. VERIFICAR VERSÃO (opcional)                      │
    │    ✓ /3/ é compatível com versão=3.13? SIM → +10  │
    │    ✗ /2/ é incompatível? → -15 pontos              │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │                  TOTAL: 90/100                       │
    │                                                     │
    │  Threshold: 60 pontos                              │
    │  Resultado: ✓ APROVADO (90 >= 60)                  │
    └─────────────────────────────────────────────────────┘
```

## Fluxo de Validação de Página

````
┌─────────────────────────────────────────────────────────────────────┐
│                       VALIDAÇÃO DE PÁGINA                           │
└─────────────────────────────────────────────────────────────────────┘

    Página: Built-in Functions — Python 3.13 Documentation
    Conteúdo: "# Functions\n\n`abs()` returns..."
              ↓
    ┌─────────────────────────────────────────────────────┐
    │ 1. VERIFICAR TAMANHO DO CONTEÚDO                    │
    │    - Página normal precisa de >= 150 chars         │
    │    - Página índice precisa de >= 50 chars          │
    │    ✓ 2547 caracteres → +20 pontos                 │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 2. VERIFICAR AUSÊNCIA DE ERRO 404                  │
    │    ✓ Título não contém "404" ou "Not Found"? → +20│
    │    ✗ "Error 404 - Page Not Found"? → REJEITA      │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 3. VERIFICAR ESTRUTURA HTML                         │
    │    Procura por:                                     │
    │    ✓ Headers (#, ##, ###) → +1                     │
    │    ✓ Código (``` ou `) → +1                        │
    │    ✓ Listas (-) → +1                               │
    │    Precisa de >= 2 elementos → +15 pontos          │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 4. VERIFICAR PALAVRAS-CHAVE INVÁLIDAS              │
    │    Bloqueia: login, carrinho, compre, fórum, blog  │
    │    ✓ Nenhuma palavra proibida? → +25               │
    │    ⚠ Uma palavra? → +10 (warning)                  │
    │    ✗ Múltiplas? → REJEITA (bloqueio)              │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │ 5. VERIFICAR PRESENÇA DE CÓDIGO                     │
    │    ✓ Tem blocos ``` ou ``` → +20                   │
    │    ⚠ Menciona código (exemplo, sample) → +10       │
    │    ✗ Sem código → 0 pontos                         │
    └──────────────────┬──────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────────────┐
    │                  TOTAL: 85/100                       │
    │                                                     │
    │  Threshold: 50 pontos                              │
    │  Resultado: ✓ APROVADA (85 >= 50)                  │
    └─────────────────────────────────────────────────────┘
````

## Matriz de Decisão - Links

```
┌──────────────────────────────────────────────────────────┐
│  CRITÉRIO       │ PONTOS │ BLOQUEIO │ FUZZY │ EXEMPLO    │
├──────────────────────────────────────────────────────────┤
│ Protocolo      │  +25   │   SIM    │  NÃO  │ https://   │
│ Domínio        │  +25   │   SIM    │  NÃO  │ *.py.org   │
│ Prefixo/Path   │  +20   │   NÃO    │  SIM  │ /3/lib/    │
│ Extensão       │  +15   │   SIM    │  NÃO  │ sem .zip   │
│ Segmentos      │  +15   │   SIM    │  SIM  │ sem /search│
│ Versão         │ ±10    │   NÃO    │  NÃO  │ v3 = 3.*   │
├──────────────────────────────────────────────────────────┤
│ MÁXIMO         │ 100    │   -      │  -    │ -          │
│ MÍNIMO         │   0    │   -      │  -    │ -          │
│ THRESHOLD      │  60    │   -      │  -    │ default    │
└──────────────────────────────────────────────────────────┘
```

## Matriz de Decisão - Páginas

```
┌──────────────────────────────────────────────────────────┐
│  CRITÉRIO           │ PONTOS │ BLOQUEIO │ FUZZY │ % MIN │
├──────────────────────────────────────────────────────────┤
│ Tamanho             │  +20   │   NÃO    │  NÃO  │ 150ch │
│ Sem 404             │  +20   │   SIM    │  NÃO  │ -     │
│ Estrutura HTML      │  +15   │   NÃO    │  NÃO  │ 2 elem│
│ Sem palavra bloq.   │  +25   │   SIM*   │  SIM  │ 0 mult│
│ Possui código       │  +20   │   NÃO    │  NÃO  │ -     │
├──────────────────────────────────────────────────────────┤
│ MÁXIMO              │ 100    │   -      │  -    │ -     │
│ MÍNIMO              │   0    │   -      │  -    │ -     │
│ THRESHOLD           │  50    │   -      │  -    │ def   │
└──────────────────────────────────────────────────────────┘
* SIM apenas se múltiplas palavras
```

## Exemplo Prático de Pontuação

### Link 1: Aprovado

```
URL: /3/library/functions.html

Protocolo: https ✓ +25
Domínio: docs.python.org ✓ +25
Prefixo: /3/library/ ✓ +20
Extensão: .html ✓ +15
Segmentos: ✓ +15
Versão: 3.x = 3.13 ✓ +10
────────────────────
TOTAL: 110 → capped at 100 → ✓ APROVADO (100 >= 60)
```

### Link 2: Rejeitado com pontuação transparente

```
URL: /3/tutorial/tutoriais  (prefixo errado)

Protocolo: https ✓ +25
Domínio: docs.python.org ✓ +25
Prefixo: /3/tutorial/ (esperado) vs /3/tutoriais/ ⚠ fuzzy 85% → +17
Extensão: (sem extensão) ✓ +15
Segmentos: ✓ +15
Versão: 3.x = 3.13 ✓ +10
────────────────────
TOTAL: 107 → capped at 100 → ✓ APROVADO

Nota: Se fosse /3/invalid/ (fuzzy 30%), teria:
Prefixo: 0 pontos → TOTAL: 80 → ✓ APROVADO (80 >= 60)
```

### Link 3: Bloqueio automático

```
URL: /search?q=functions

Protocolo: https ✓ +25
Domínio: docs.python.org ✓ +25
Prefixo: ✓ +20
Extensão: ✓ +15
Segmentos: /search ✗ BLOQUEIO AUTOMÁTICO
────────────────────
TOTAL: 0 → ✗ REJEITADO (motivo específico: "/search é proibido")

Nota: Nem precisa calcular outros critérios após bloqueio
```

## Distribuição de Threshold Recomendada

```
100 ┤
    │
 90 ├──────────────────────────────────────────────
    │     Excelentes
    │     (Documentação oficial de primeira linha)
 75 ├──────────────────────────────────────────────
    │     Bons
    │     (Documentação válida, alguns desvios)
 60 ├────────────────────────────────────────────── ← THRESHOLD PADRÃO
    │     Aceitáveis
    │     (Válidos mas com pequenas irregularidades)
 50 ├──────────────────────────────────────────────← THRESHOLD FLEXÍVEL
    │     Borderline
    │     (Procure revisar)
 25 ├──────────────────────────────────────────────
    │     Suspeitos
    │     (Muitos problemas detectados)
  0 ├──────────────────────────────────────────────
    └─────────────────────────────────────────────
    Probabilidade de ser realmente relevante
```

## Comparativo: Método Antigo vs Novo

```
MÉTODO ANTIGO (Binário)          │ MÉTODO NOVO (Pontuação)
─────────────────────────────────┼──────────────────────────────
                                 │
✓ APROVADO                       │ ✓ APROVADO (90/100)
✗ REJEITADO                      │ ✗ REJEITADO (35/100)
                                 │ ⚠ BORDERLINE (58/100)
                                 │
Sem informação sobre por quê     │ Detalhes sobre cada critério
Não há "cinza"                   │ Flexibilidade com limiares
Difícil ajustar                  │ Fácil ajustar threshold
                                 │
Falsos positivos: altos          │ Falsos positivos: baixos
Falsos negativos: altos          │ Falsos negativos: baixos
```

## Fluxo de Integração no Seu Crawler

```
┌─────────────────────────────────────────────────────────┐
│               CRAWLING DE DOCUMENTAÇÃO                  │
└─────────────────────────────────────────────────────────┘

    URLs_para_acessar = [url1, url2, url3, ...]
              ↓
    ┌─────────────────────────────────┐
    │ Para cada URL em batch:         │
    │ validar_link_novo_com_pontuacao │
    └─────────────┬───────────────────┘
                  ↓
         ┌────────────────┐
         │ Score >= 60?   │
         └────┬───────┬───┘
              │       │
         SIM  │       │ NÃO
              ↓       ↓
         ┌──────┐ ┌─────────────┐
         │ Acessar│ Rejeitar e  │
         │ página │ logar razão │
         └───┬──────┘ └─────────────┘
             ↓
    ┌─────────────────────────────────┐
    │ Extrair conteúdo e converter    │
    │ para Markdown                   │
    └─────────────┬───────────────────┘
                  ↓
    ┌─────────────────────────────────┐
    │ Para página extraída:           │
    │ validar_pagina_atual_com_pontuacao
    └─────────────┬───────────────────┘
                  ↓
         ┌────────────────┐
         │ Score >= 50?   │
         └────┬───────┬───┘
              │       │
         SIM  │       │ NÃO
              ↓       ↓
         ┌──────┐ ┌─────────────┐
         │ Salvar│ Descartar e  │
         │ JSON  │ logar razão  │
         └──────────┘ └─────────────┘
```
