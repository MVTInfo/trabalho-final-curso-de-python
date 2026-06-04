# trabalho-final-curso-de-python - API

API RESTful desenvolvida em Python com **FastAPI** e **Pandas** para análise e estatística de dados de vendas.

O projeto possue arquitetura em camadas (  

    Model,  

    Repository,  

    Service,  

    Controller  

).


# Funcionalidades

**Filtros**:      Listagem geral de vendas, busca por categoria e cidade.  

**Estatísticas**: Faturamento total, ticket médio.  

**Comercial**:    Ranking Top 10 produtos mais vendidos, ranking por cidades e faturamento e vendas por forma de pagamento.  

**Arquivos**:     Exportação dos dados em formato CSV e endpoint para upload da base de dados com validação de estrutura.  


# Tecnologias Utilizadas

**Python**  

**FastAPI**:       Framework web de alta performance.  

**Pandas**:        Manipulação e análise de dados em nível de performance C.  

**Pydantic**:      Validação de contratos de dados (Schemas).  

**Uvicorn**:       Servidor ASGI para rodar a aplicação.  

**Python-Dotenv**: Gerenciamento de variáveis de ambiente.  


# Instalar o Python

```Caso não seu computador não tenha o python instalado acesse o site abaixo para baixar a versão recomendada para o seu Sistema Operacional.```


***https://www.python.org/downloads/***    

# Como Executar o Projeto

```Após clonar ou extrair o projeto execute os seguintes comandos.```

    python -m venv .venv
---
    .venv\Scripts\Activate.ps1
---
    .venv\Scripts\activate.bat

*Caso a execução de scripts esteja desibilitada no seu computador.*

Alterar a política para o usuário atual (Recomendado). Esta é a solução permanente mais segura. Ela não requer privilégios de administrador e permite que ferramentas locais (como Node.js, ambientes virtuais Python ou VS Code) executem scripts corretamente.

 *Execute o comando abaixo no PowerShell:*

    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

```Instalar as Dependências```
    
    pip install fastapi uvicorn pandas python-dotenv python-multipart pydantic

```Variáveis de Ambiente```

Criar arquivo **`.env`** na raiz do projeto:

    DATABASE_PATH=./data
    
    DATABASE_FILE_NAME=sales-file.csv

```Inicialização```

```Execute o servidor Uvicorn:```

    uvicorn main:app --reload


# Documentação da API (Swagger)

Confira a documentação da API pelo Swagger acessando o navegador no endereço:

***http://127.0.0.1:8000/docs***


# Camada de Segurança (Data Cleansing)

A api conta com funcionalidade verificação dos dados e colunas do arquivo csv;  

Uploads de arquivos somente com extensão *.csv;  

Tratamento dos campos como: remossão de dízimas;  

Conversão de datas para o padrão internacional `AAAA-MM-DD`;  

Tratamento de campos nulos.