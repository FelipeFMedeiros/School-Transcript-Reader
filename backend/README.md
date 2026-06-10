# Arquitetura e Pipeline do Compilador (Back-end)

O back-end do **School Transcript Reader** é o coração da aplicação, responsável por processar os históricos escolares e expor os resultados de forma estruturada.

Ele foi desenvolvido em **Python**, utilizando o framework **Django** junto com o **Django REST Framework (DRF)** para a construção rápida e segura da API.

## O Pipeline de Compilação (`compiler-engine`)

A lógica principal do sistema não é um simples parse de strings, mas sim um fluxo clássico de um compilador adaptado para extração de dados:

1. **Extração Bruta:** 
   Utilizamos bibliotecas especializadas (como `pdfplumber` ou `PyMuPDF`) para ler o PDF recebido pela API e extrair o texto de maneira estruturada.
2. **Analisador Léxico (Scanner):** 
   O texto bruto passa por uma série de Expressões Regulares mapeadas por Autômatos Finitos. O analisador descarta espaços em branco irrelevantes e transforma a string em uma lista de **Tokens**. Caso um caractere não reconhecido seja encontrado, a compilação é interrompida com um *Erro Léxico*.
3. **Analisador Sintático (Parser):** 
   A lista de tokens gerada é consumida aplicando uma **Gramática Livre de Contexto**. Se a estrutura do histórico estiver fora da ordem ou regra definida, a compilação retorna um *Erro Sintático*.
4. **Analisador Semântico:** 
   Com a árvore sintática gerada, verificamos a coerência das informações (ex: se a carga horária está correta, ou se as notas fazem sentido). Inconsistências geram *Erros Semânticos*.
5. **Persistência de Dados e Resposta:** 
   Se todas as fases passarem sem erros, os dados do aluno (Nome, Matrícula, IRA, Disciplinas Cursadas) são convertidos em JSON, salvos no banco de dados **PostgreSQL** e retornados como resposta de sucesso (`status 201`).

## Estrutura da API

A API segue o padrão RESTful. A documentação completa dos esquemas e payloads pode ser visualizada no arquivo OpenAPI do projeto (`api-schema.yaml` na raiz do repositório) ou acessando o Swagger gerado automaticamente quando a aplicação estiver rodando (`http://localhost:8000/api/docs`).

As rotas principais incluem:
- `GET /api/histories/` - Lista o histórico das análises realizadas (com paginação).
- `GET /api/histories/{id}/` - Retorna a árvore completa, tabela de símbolos, dados acadêmicos ou erros de uma análise específica.
- `POST /api/histories/` - Endpoint que recebe o arquivo PDF (via *multipart/form-data*) e inicia todo o pipeline de compilação.
- `DELETE /api/histories/{id}/` - Apaga o registro da análise do banco de dados.