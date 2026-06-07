# Arquitetura e Pipeline do Compilador (Back-end)

## Fase 2: Arquitetura e Stack Tecnológica

A divisão do projeto em 3 estruturas deixará o sistema organizado e mais fácil de apresentar:

* **Back-end (API + Compilador):** Python (com frameworks como FastAPI, Flask ou Django) para expor as rotas da API. Será utilizado bibliotecas como `pdfplumber` ou `PyMuPDF` para extrair texto bruto dos PDFs de forma estruturada.
* **Banco de Dados:** PostgreSQL para persistir os dados acadêmicos extraídos (quando o histórico for validado).
* **Front-end (Visualização):** Interface construída com React e TypeScript, utilizando TailwindCSS e shadcn/ui para a estilização, de forma moderna, limpa e reativa. Componentes para fazer o upload do PDF e exibir painéis com os resultados da análise.

---

## Fase 3: Implementação do Pipeline do Compilador no Back-end

O coração do projeto ficará na API Python, que deve processar o documento nas seguintes etapas:

1. **Extração:** 
   Ler o PDF recebido pelo front-end e extrair o texto bruto.

2. **Analisador Léxico (Scanner):** 
   Transformar o texto bruto em uma lista de tokens, descartando espaços em branco irrelevantes. Se encontrar um caractere ou padrão não mapeado, gerar um erro léxico.

3. **Analisador Sintático (Parser):** 
   Consumir a lista de tokens aplicando a gramática definida (ex: via descida recursiva). Se a estrutura do histórico estiver fora de ordem, gerar um erro sintático.

4. **Analisador Semântico:** 
   Validar a coerência das informações extraídas pela árvore sintática.

5. **Saída de Dados:** 
   Se não houver erros nas três fases, estruturar os dados (aluno, matrícula, disciplinas) em JSON, salvar no PostgreSQL e enviar como resposta de sucesso para o front-end.