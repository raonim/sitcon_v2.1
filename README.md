# SITCON - Sistema de Informações de Trajeto de Condutores

O **SITCON** é uma aplicação web desenvolvida em Flask voltada para a gestão e consulta de informações técnicas sobre equipamentos ferroviários, especificamente Aparelhos de Mudança de Via (AMV), Circuitos de Via (CDV) e Sinais. O sistema permite a visualização detalhada de registros técnicos, localização geográfica de ativos e a importação de dados via arquivos CSV.

## 🚀 Funcionalidades

### 1. Gestão de Equipamentos
O sistema organiza as informações em três categorias principais:
* **AMV (Aparelhos de Mudança de Via):** Consulta de comandos (NWR/WR) e indicações (NWP/WP), com suporte a coordenadas geográficas fixas para visualização no mapa.
* **CDV (Circuitos de Via):** Detalhamento técnico de ocupação e detecção de via.
* **Sinais:** Informações sobre aspectos e sinalização de via.


### 2. Segurança e Acesso
* Sistema de login com autenticação de usuários via hash de senha.
* Controle de acesso protegido por decoradores que exigem sessão ativa (`@login_required`).
* Validação de cadastro baseada em uma lista de matrículas previamente autorizadas no sistema.

### 3. Formatação Dinâmica
* Tradução automática de termos técnicos do banco de dados para nomes amigáveis ao usuário (ex: `idamv` vira "AMV", `idSinais` vira "SINAL").
* Formatador de locações que converte códigos internos (ex: "B-B-29") em descrições legíveis como "Caixa B, TB B-29".

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.13 com o framework Flask.
* **Banco de Dados:** SQLite integrado via Flask-SQLAlchemy.
* **Frontend:** Jinja2 (Templates), Bootstrap 5 (Estilização) e ícones via Bootstrap Icons.
* **Segurança:** Werkzeug para geração e verificação de hashes de senhas.

## 📂 Estrutura Principal do Projeto

* `app.py`: Arquivo principal contendo as rotas, lógica de negócio e configurações do Flask.
* `models.py`: Definição dos modelos do banco de dados (ORM) para Equipamentos, Usuários e Matrículas.
* `requirements.txt`: Lista de dependências e bibliotecas necessárias para o projeto.
* `templates/`: Arquivos HTML organizados de forma modular utilizando herança de template (`base.html`).
* `static/`: Recursos estáticos como arquivos CSS, JavaScript e imagens dos equipamentos.

## 🔧 Como Executar

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Inicialize o banco de dados:**
    O sistema cria automaticamente o arquivo `sitcon.db` e as tabelas necessárias ao ser executado pela primeira vez.

3.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    A aplicação estará disponível por padrão em `http://127.0.0.1:5000`.

---
*Versão 1.0 | © 2025 SITCON*
