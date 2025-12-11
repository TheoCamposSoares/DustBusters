# DustBusters

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2025.2  
**Professor:** Andre Luis Fonseca Faustino  
**Turma:** T04

## Integrantes do Grupo
* Theo Campos Soares (20240016648)
* Yasmin Maria Lima Aires de Carvalho (20240013181)
* Saulo Carlos Pereira da Rocha (20240020687)

## Descrição do Projeto
Entender do que se trata Inteligência Artificial requer compreender uma série de definições fundamentais que permeiam esse ramo da tecnologia. A definição de agente inteligente, por exemplo, é alimentada a partir de diferentes tipos de agentes (como um agente reativo simples ou um agente baseado em objetivo), algoritmos que diferem em arquitetura e na forma como os problemas são resolvidos. No contexto de ensino e aprendizagem, observar a funcionalidade de um certo tipo de agente em um simulador visual-interativo tende a maximizar a compreensão desse conceito pelos discentes e dinamizar parte da execução da disciplina pelo docente.

Diante disso, o presente trabalho tem como objetivo o desenvolvimento de uma plataforma visual didático interativa que elucida, de forma mais clara e atrativa, as definições de agente reativo simples e agente baseado em objetivo. Para isso, utilizamos a linguagem de programação Python e duas principais bibliotecas relacionadas: PyGame e Pytest. Além disso, para atingirmos a implementação efetiva do algoritmo de agente baseado em objetivo, aplicamos o algoritmo de busca heurística A* em conjunto com cálculo da Distância Manhattan.

## Guia de Instalação e Execução

### 1. Instalação das Dependências
Certifique-se de ter o **Python 3.12** instalado ([https://www.python.org/downloads/](https://www.python.org/downloads/)). Clone o repositório e instale as bibliotecas listadas no `requirements.txt`:

```bash
# Clone o repositório
git clone https://github.com/TheoCamposSoares/DustBusters.git

# Entre na pasta do projeto
cd DustBusters

# Instale as dependências
pip install -r requirements.txt
````

### 2. Como Executar a aplicação

Execute o comando abaixo no terminal para iniciar o servidor local:

```bash
python -m src.main
```

### 3. Como Executar os testes

Execute o comando abaixo no terminal:

```bash
pytest -v
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

  * Stuart Russell and Peter Norvig. Artificial Intelligence: A Modern Approach, 4th US ed.
