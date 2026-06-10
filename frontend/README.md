# Interface e Visualização do Compilador (Front-end)

O front-end do **School Transcript Reader** é a camada de interação do usuário com a API, focado em apresentar os resultados do pipeline de compilação de forma didática, limpa e moderna.

## Funcionalidades Principais

1. **Upload Interativo:** Área de *drag-and-drop* intuitiva para enviar o histórico escolar (PDF) para a API, com feedback visual integrado.
2. **Dashboard de Resultados:** Em caso de sucesso (`status: success`), apresenta de forma organizada e centralizada os dados acadêmicos do aluno (Nome, IRA, Histórico de Disciplinas).
3. **Console de Erros:** Caso o compilador do back-end pare no meio do processo, o front-end mapeia exatamente a fase (Léxica, Sintática ou Semântica), a linha e a mensagem de erro da falha.
4. **Tabela de Símbolos Volátil:** Painel exclusivo de *Debug* exibindo de forma interativa a saída gerada pelo analisador léxico, com IDs, tokens identificados, valores e número da linha.

## Stack Tecnológica

O projeto foi construído usando ferramentas modernas do ecossistema JavaScript/TypeScript:

- **Core:** React 19 + TypeScript, orquestrados através do Vite para máxima performance de build.
- **Estilização e UI:** Tailwind CSS (v4) para estilização fluida, complementado por componentes reutilizáveis acessíveis inspirados no shadcn/ui.
- **Consumo da API:**
  - **Axios:** Cliente HTTP principal, configurado no diretório `src/services/` para gerenciar a URL base, requisições paginadas e uploads *multipart/form-data*.
  - **Serviços Tipados (`src/types/api.ts`):** Todos os modelos retornados pela API (como `DocumentDetail` e `CompilerError`) são tipados de acordo com o esquema Swagger (`api-schema.yaml`).
- **Gerenciamento de Estado Global:** Utilizamos o **Zustand** (`src/store/compilerStore.ts`) para sincronizar a lista de históricos em tempo real e orquestrar as requisições assíncronas do Axios sem a necessidade de *prop-drilling*.

## Arquitetura de Pastas

- **`/src/components/`**: Componentes reutilizáveis como `UploadZone`, `SuccessDashboard`, `SymbolTable` e fragmentos da UI base.
- **`/src/pages/`**: Telas principais da aplicação (Página de Históricos, Página de Resultado com sistema de *Tabs* e Página de Upload).
- **`/src/services/`**: Camada isolada de comunicação com o Back-end. Contém as configurações do Axios e os métodos REST encapsulados (`HistoriesService`).
- **`/src/types/`**: Definições das interfaces e contratos TypeScript da API.
- **`/src/store/`**: Estado global da aplicação com Zustand.

## Como rodar localmente (Modo Desenvolvimento isolado)

Caso você não queira rodar o projeto todo via Docker Compose e precise alterar o código front-end isoladamente, nós utilizamos o **Bun** como gerenciador:

**Pré-requisitos:**
- [Bun](https://bun.sh/) instalado (versão **v1.3.x**)

**Passo a passo:**
1. Navegue até o diretório raiz do front-end (`/frontend`).
2. Instale as dependências:
   ```bash
   bun install
   ```
3. Inicie o servidor de desenvolvimento Vite:
   ```bash
   bun dev
   ```
4. A aplicação abrirá em `http://localhost:5173`. Para que a integração de dados e uploads funcione, o back-end (Django) precisa estar rodando simultaneamente (por padrão, na porta `8000`).