# Selenium Project – Web Scraping  
> Projeto de automação e extração de dados utilizando Selenium  

## 🚀 Visão Geral  
Este repositório contém um conjunto de scripts desenvolvidos em Python que utilizam a biblioteca Selenium para automatizar navegação web e extrair dados de diferentes fontes. O objetivo é demonstrar práticas de web scraping dinâmico (com interação, rolagem, formulários, etc.), captura de dados, tratamento e exportação para formatos utilizáveis.

## 💡 Principais Funcionalidades  
- Automação de navegação, login, preenchimento de formulários e clique em elementos da página (script: `preenchimento_forms.py`).  
- Busca e extração de perfis (script: `buscador_perfis.py`).  
- Busca com cadastro automático de perfis em determinado sistema (script: `buscar_cadastrar_perfis.py`).  
- Filtro e extração de produtos de uma loja ou marketplace (script: `buscar_produtos_filtrados.py`).  
- Captação de dados de criptomoedas via site, exportando CSV/JSON (script: `captar_cripto.py`).  
- Armazenamento dos dados extraídos em arquivos como `dados_capturados.csv`, `dados_capturados.json` e outros desafios realizados (`desafio_1.json`, `desafio_2.json`, etc.).  
- Exemplo de pipeline: extrair → tratar → salvar → reutilizar.

## 📦 Tecnologias Utilizadas  
- Linguagem: Python (versão 3.x)  
- Automação web: Selenium  
- Exportação de dados: CSV, JSON  
- Estrutura de projeto simples, com scripts independentes para diferentes casos de uso  
- Virtualenv para isolamento de dependências (exemplo de pastas: `venv/`)

## 🧭 Como Rodar o Projeto  
### Pré-requisitos  
1. Instalar Python 3.x no sistema.  
2. Instalar o navegador compatível (por exemplo, Chrome) e o driver correspondente (ex: chromedriver) configurado no PATH ou especificado no código.  
3. Criar e ativar um ambiente virtual (opcional, mas recomendado):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux / Mac
   venv\Scripts\activate       # Windows
