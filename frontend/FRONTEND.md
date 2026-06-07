# Interface e Visualização do Compilador (Front-end)

## Fase 4: Desenvolvimento do Front-end Interativo

O objetivo principal do front-end é apresentar o funcionamento interno do compilador de forma visual, educacional e clara, permitindo o acompanhamento de cada etapa da análise do histórico escolar.

### Funcionalidades Essenciais

1. **Upload de Documentos (PDF):**
    - Área de envio intuitiva (drag-and-drop) para receber o histórico escolar.
    - Feedback visual de processamento (loading/spinner) enquanto aguarda a resposta e análise do back-end.

2. **Tabela de Símbolos Volátil:**
    - Criação de uma tabela interativa que é preenchida com os dados processados.
    - Permite visualizar os tokens identificados e o comportamento interno do scanner de forma didática.

3. **Exibição e Rastreamento de Erros:**
    - Caso o back-end retorne inconsistências, a interface destacará exatamente onde e por que o compilador falhou.
    - Tratamento visual padronizado para os três tipos de falhas:
        - **Erro Léxico:** Identificação de caracteres desconhecidos.
        - **Erro Sintático:** Estrutura do documento fora da ordem esperada pela gramática.
        - **Erro Semântico:** Informações incoerentes (ex: soma de carga horária inválida).

4. **Dashboard de Sucesso:**
    - Se o documento for válido nas três fases da compilação, exibiremos os dados acadêmicos estruturados de forma clara.
    - Cartões (cards) organizados contendo: informações do aluno, matrícula, disciplinas cursadas, status e semestres.

### Stack Tecnológica e Ferramentas

- **Framework Base:** React com TypeScript configurado via Vite para máxima performance.
- **Estilização e UI:** TailwindCSS combinado com os componentes pré-fabricados do `shadcn/ui` para construção ágil (botões, modais, tabelas, notificações).
- **Gerenciamento de Estado:** Utilização do Zustand (já presente no projeto) para manter a fluidez entre o status do upload, progresso da compilação, e dados retornados da API.
