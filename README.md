# [DustBusters]

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2025.2  
**Professor:** Andre Luis Fonseca Faustino  
**Turma:** T04

## Integrantes do Grupo
* Theo Campos Soares (20240016648)
* Yasmin Maria Lima Aires de Carvalho (20240013181)
* Saulo Carlos Pereira da Rocha (20240020687)

## Descrição do Projeto
[Descreva aqui em 1 ou 2 parágrafos a proposta do projeto e as tecnologias utilizadas para seu desenvolvimento]

## Guia de Instalação e Execução

### 1. Instalação das Dependências
Certifique-se de ter o **Python 3.12** instalado. Clone o repositório e instale as bibliotecas listadas no `requirements.txt`:

```bash
# Clone o repositório
git clone [https://github.com/TheoCamposSoares/DustBusters.git](https://github.com/TheoCamposSoares/DustBusters.git)

# Entre na pasta do projeto
cd DustBusters

# Instale as dependências
pip install -r requirements.txt
````

### 2. Como Executar

Execute o comando abaixo no terminal para iniciar o servidor local:

```bash
python -m src.main
```

## Estrutura dos Arquivos

  * `src/`: Código-fonte da aplicação (agentes, ambientes, simulação, UI e main).
    * `agentes/`: Código dos agentes (classe base, agente simples e agente baseado em objetivo).
    * `ambientes/`: Código dos ambientes (classe base, ambiente 1x2 e ambiente 7x7).
    * `simulação/`: Lógica agente/ambiente.
    * `ui/`: Telas, botões e estilos.
    * `main.py`: Gerenciamento principal.
  * `docs/`: PEAS dos dois agentes (arquivos markdown).
  * `tests/`: Testes de agentes e ambientes (pytest)
  * `assets/`: Backgrounds, sprites, prints e fonte.

## Resultados e Demonstração

![Tela do menu](./assets/print_menu.png)
![Tela do jogo](./assets/print_simples.png)
![Tela do jogo](./assets/print_objetivo.png)
![Tela final](./assets/print_fim.png)

## Referências

  * [Stuart Russell and Peter Norvig. Artificial Intelligence: A Modern Approach, 4th US ed.]