# Gerenciador de Tarefas WEB

Aplicação web para gerenciamento de tarefas, construída com Python e Streamlit. Permite adicionar, visualizar, filtrar, concluir e deletar tarefas, com um gráfico de status em tempo real.

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)

## Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/joaoamado29/Gerenciador-de-Tarefas-WEB.git
cd Gerenciador-de-Tarefas-WEB
```

**2. Crie e ative o ambiente virtual**

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

## Executando

```bash
streamlit run app.py
```

O app abrirá automaticamente no navegador em `http://localhost:8501`.

## Funcionalidades

- **Adicionar tarefa** — nome, status (Pendente/Concluído) e data de vencimento, pela barra lateral
- **Listar tarefas** — tabela com todas as tarefas cadastradas
- **Concluir tarefa** — marca uma tarefa como concluída
- **Deletar tarefa** — remove uma tarefa permanentemente
- **Filtrar por status** — exibe apenas tarefas Pendentes ou Concluídas
- **Gráfico de status** — gráfico de barras com a contagem por status

## Estrutura do projeto

```
├── app.py                        # Ponto de entrada
├── requirements.txt              # Dependências
├── database/
│   ├── connection.py             # Conexão com o SQLite
│   └── migrations.py            # Criação das tabelas
├── models/
│   └── task.py                  # Modelo Task e enum TaskStatus
├── repositories/
│   └── task_repository.py       # Operações de banco de dados
└── ui/
    ├── sidebar.py               # Formulário de adição
    ├── task_list.py             # Listagem e ações
    └── charts.py                # Gráfico de status
```

## Testes

Instale as dependências de desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

Rode os testes:

```bash
pytest -v
```

Os testes usam um banco SQLite temporário isolado — não afetam o `tasks.db` local.

## Banco de dados

O banco SQLite (`tasks.db`) é criado automaticamente na raiz do projeto ao executar o app pela primeira vez. Para usar um caminho diferente, defina a variável de ambiente:

```bash
DB_PATH=/caminho/para/banco.db streamlit run app.py
```
