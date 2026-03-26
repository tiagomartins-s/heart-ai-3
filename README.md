# 🫀 HeartAI 3 — Assistente Cardiológico Conversacional (CardioIA Fase 5)

## 📋 Sobre o Projeto

O **HeartAI 3** é um protótipo funcional de **Assistente Cardiológico Inteligente e Conversacional**, desenvolvido para simular um atendimento inicial em saúde por meio de **Processamento de Linguagem Natural (NLP)** e **automação de fluxos**.

O assistente foi modelado no **IBM Watson Assistant** e integrado a um **backend Python (Flask)**, que permite que o usuário converse com o sistema via uma **interface simples em HTML**.

> Observação importante: este projeto é educacional e **não substitui atendimento médico**. Em casos de sintomas compatíveis com emergência, o assistente orienta o usuário a buscar ajuda imediatamente.

## 🎯 Objetivo Geral da Fase 5

Construir um chatbot que:

- interaja com o usuário usando linguagem natural;
- interprete intenções (intents) de forma estruturada;
- apresente respostas contextualizadas e organizadas;
- integre o Watson Assistant com um backend simples;
- forneça uma interface funcional para envio e visualização de mensagens.

## 🏗️ Arquitetura do Sistema

### Visão geral

1. **Front-end (HTML/JS)**: captura a mensagem do usuário e envia ao backend.
2. **Backend (Flask)**: recebe a mensagem, mantém o `context` da conversa e faz a chamada à API do Watson.
3. **IBM Watson Assistant**: identifica a intenção e retorna a resposta conforme os `dialog_nodes`.

### Fluxo conversacional no Watson Assistant

O arquivo `watson.json` contém a configuração exportada do assistente, incluindo:

- **Intents**
  - `emergencia_cardiaca`: triagem quando o usuário descreve dor no peito/aperto/falta de ar grave.
  - `agendar_exame`: orientação para agendamento (ex.: eletrocardiograma, ecocardiograma, holter).
  - `duvida_pressao`: dúvidas sobre pressão arterial.
  - `duvida_sintomas`: como reconhecer sintomas gerais relacionados a problemas cardiológicos.
- **Dialog nodes**
  - `node_welcome`: mensagem inicial ao iniciar a conversa (`conditions: "welcome"`).
  - `node_emergencia`: resposta de alerta para `#emergencia_cardiaca`.
  - `node_exames`: resposta para `#agendar_exame`.
  - `node_pressao`: resposta para `#duvida_pressao`.
  - `node_duvida_sintomas`: resposta para `#duvida_sintomas`.
  - `node_anything_else`: *fallback* para entradas não compreendidas (`conditions: "anything_else"`).

### Integração backend ↔ Watson

O backend em `app.py` utiliza:

- `AssistantV1` do `ibm-watson`
- `IAMAuthenticator` do `ibm-cloud-sdk-core`
- endpoint `/api/mensagem` para troca de mensagens

O backend mantém o estado da conversa retornando e reutilizando o `context` do Watson entre requisições.

### Conceitos Utilizados (NLP e Chatbots)

- **Intents**: representam o “objetivo” da mensagem do usuário (ex.: emergência, agendamento, dúvida).
- **Dialog nodes**: definem o fluxo e a resposta retornada pelo Watson quando uma intenção é identificada.
- **Contexto (`context`)**: estrutura retornada pelo Watson usada pelo front-end/back-end para manter o estado da conversa entre mensagens.
- **Fallback (`anything_else`)**: reduz respostas inadequadas quando o usuário foge do escopo do assistente.

### O que foi Implementado Nesta Entrega

- Fluxo conversacional para triagem e orientação inicial com as intenções:
  - `emergencia_cardiaca`
  - `agendar_exame`
  - `duvida_pressao`
  - `duvida_sintomas`
- Backend Flask com endpoint:
  - `/api/mensagem` (POST) para trocar mensagens com o Watson e preservar `context`
- Interface web simples (chat) em `templates/index.html`:
  - mantém `watsonContext`
  - renderiza mensagens do usuário e do assistente
- Arquivo de exportação do assistente:
  - `watson.json` (modelo de intents e dialog nodes para doc/reprodução no Watson)

### Endpoint `/api/mensagem`

Requisição (JSON):

```json
{
  "mensagem": "texto do usuário",
  "context": {}
}
```

Resposta (JSON):

```json
{
  "resposta": "texto do assistente",
  "context": {}
}
```

## 🚀 Como Executar

### Pré-requisitos

1. Python instalado (recomendado Python 3.9+)
2. Acesso ao IBM Watson Assistant (Plano compatível com API Lite ou com acesso liberado)

### Dependências

No diretório do projeto:

```bash
pip install -r requirements.txt
```

### Credenciais (recomendado via variáveis de ambiente)

Configure:

- `WATSON_API_KEY`
- `WATSON_URL`
- `WATSON_WORKSPACE_ID`

Exemplo (ajuste para seu ambiente):

```bash
set WATSON_API_KEY="SUA_CHAVE"
set WATSON_URL="SUA_URL"
set WATSON_WORKSPACE_ID="SEU_WORKSPACE_ID"
```

> Dica: evite hardcode de chaves em commits. O `app.py` possui valores *fallback* apenas para facilitar o funcionamento local; use variáveis de ambiente em produção/publicação.

### Iniciar o servidor Flask

```bash
python app.py
```

O servidor sobe em `http://localhost:5000`.

### Usar a interface

1. Abra `http://localhost:5000/`
2. Envie mensagens no chat
3. O sistema processa a intenção no Watson e devolve a resposta

## 📌 Cenários de Demonstração (Teste Rápido)

- Emergência: envie “Estou com muita dor no peito” e observe o alerta para procurar urgência.
- Agendamento: envie “Quero agendar um ecocardiograma” e observe a orientação de agenda.
- Pressão arterial: envie “A minha pressão está 15 por 9, o que faço?” e observe a orientação inicial.
- Sintomas: envie “Quais os sintomas de um infarto?” e observe a lista de sintomas e a pergunta de triagem.

## 📁 Estrutura de Arquivos

```
heart-ia-3/
├── app.py                          # Backend Flask + integração com IBM Watson
├── requirements.txt               # Dependências do projeto
├── watson.json                    # Export do IBM Watson Assistant (intents e dialog nodes)
└── templates/
    └── index.html                 # Interface do chat (HTML + JS)
```

## 🔒 Boas Práticas e Governança (Saúde e Segurança)

- **Alertas de emergência**: o assistente contém um fluxo específico (`emergencia_cardiaca`) para orientar busca imediata de atendimento em casos compatíveis com risco.
- **Transparência**: o comportamento do chatbot é documentado na configuração exportada (`watson.json`).
- **Limitações**: respostas são geradas a partir de intents/regras do assistente; o sistema não diagnostica clinicamente e não substitui avaliação profissional.
- **Qualidade do fluxo**: há tratamento básico para entradas fora do escopo (`anything_else`) para reduzir respostas inadequadas.

## 📄 Relatório da Fase 5

O relatório complementar do trabalho (1–2 páginas, conforme a atividade) foi adicionado como:

- `relatorio.docx` (na raiz do projeto)

Esse documento descreve o funcionamento do fluxo conversacional, a integração do backend com o Watson e exemplos de cenários de interação.

