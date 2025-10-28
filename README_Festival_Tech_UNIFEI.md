# Festival Tech UNIFEI — Bilheteria & Roteiro de Estandes

**Disciplina:** ECOP06 — Python, Orientação a Objetos e Estrutura de Dados  
**Professora:** Bárbara Pimenta Caetano  
**Instituição:** UNIFEI — Instituto de Engenharia de Sistemas e Tecnologias da Informação (IESTI)

---

## Integrantes
- Renan Rangel da Silva — 2025013764  
- Lucas Fernandes Faria — 2025006840

---

## Descrição
Aplicação em **Python 3** que implementa um terminal de comandos para simular duas frentes de um festival universitário:

1. **Bilheteria & Portaria** — gerenciamento de ingressos e atendimento em fila, com dois modos:
   - **MODO PADRAO**: fila única (FIFO).
   - **MODO PRIORIDADE**: três filas (VIP → INTEIRA → MEIA), mantendo ordem de chegada dentro de cada categoria.

2. **Roteiro do Visitante** — navegação entre estandes com comandos `IR`, `VOLTAR` e `AVANCAR`, utilizando pilhas (histórico).

3. **Histórico de Ações (DESFAZER / REFAZER)** — ações que alteram estado (ex.: `COMPRAR`, `ENTRAR`, `CANCELAR`, `MODO`, `IR`, `VOLTAR`, `AVANCAR`) são registradas para permitir desfazer e refazer.

---

## Estrutura do Projeto
```
festival-tech/
├─ fila.py          # Operações da bilheteria (fila padrão e prioridade)
├─ pilha.py         # Pilhas e suporte a desfazer/refazer
├─ ingressos.py     # Modelo de ingresso e estatísticas
├─ roteiro.py       # Comandos de navegação (IR/VOLTAR/AVANCAR/ONDE/MAPA)
├─ terminal.py      # CLI: loop principal que interpreta comandos
├─ README.md        # Este arquivo
└─ RELATORIO.pdf    # Relatório com conceitos, arquitetura e demonstrações
```

---

## Requisitos (como o programa funciona)
- **Fila:** implementada com `collections.deque` (eficiente para `append`/`popleft`).  
- **Pilhas:** implementadas com listas nativas (`append`/`pop`).  
- **Histórico (undo/redo):** duas pilhas separadas (undo/redo).  
- **Modelagem:** ingressos e estado são representados por dicionários/objetos simples.  
- **Interface:** prompt interativo que lê um comando por linha.  
- **Bibliotecas:** apenas a biblioteca padrão do Python (conforme o enunciado).

---

## Como executar
1. Tenha Python 3 instalado (recomendado 3.8+).  
2. No terminal, navegue até a pasta do projeto `festival-tech`.  
3. Execute:
```bash
python terminal.py
```
4. Você verá um prompt `>`. Digite `AJUDA` para ver a lista completa de comandos.

---

## Comandos (resumo)
- `COMPRAR <nome> <categoria>` — cria um ingresso (categorias: `INTEIRA`, `MEIA`, `VIP`) e enfileira.  
- `ENTRAR` — atende o próximo visitante (remove da fila e exibe os dados).  
- `ESPIAR` — mostra quem será atendido em seguida (sem remover).  
- `CANCELAR <id>` — cancela um ingresso pendente (identificado pelo id).  
- `LISTAR` — lista os ingressos pendentes na ordem de atendimento.  
- `ESTATISTICAS` — mostra total pendente/atendido, contagem por categoria e tempo médio de espera (relógio lógico: cada `ENTRAR` conta 1 minuto).  
- `MODO PADRAO` / `MODO PRIORIDADE` — alterna o modo de atendimento.  
- `IR <caminho>` — navega para um estande (caminho absoluto ou relativo). Empilha o local atual em `VOLTAR` e limpa `AVANCAR`.  
- `VOLTAR` / `AVANCAR` — navegação entre locais usando pilhas.  
- `ONDE` — mostra o local atual.  
- `DESFAZER` / `REFAZER` — desfaz/refaz a última ação que alterou estado.  
- `AJUDA` — exibe ajuda com os comandos.  
- `SAIR` — encerra o programa.  

> Observação: comandos de consulta (`ESPIAR`, `LISTAR`, `ESTATISTICAS`, `ONDE`) **não** entram no histórico de desfazer/refazer.

---

## Exemplos de uso (sessão de terminal)
```
> AJUDA
Comandos: COMPRAR/ENTRAR/ESPIAR/CANCELAR/LISTAR/ESTATISTICAS/MODO/IR/VOLTAR/AVANCAR/ONDE/DESFAZER/REFAZER/SAIR

> COMPRAR Ana VIP
OK: ingresso 1

> COMPRAR Bruno INTEIRA
OK: ingresso 2

> MODO PRIORIDADE
OK

> ENTRAR
Entrada: [1] Ana (VIP)

> DESFAZER
OK: desfaz ENTRAR (ingresso 1 retorna à fila VIP)

> IR /Palco
OK: /Palco

> IR /IA/Visao
OK: /IA/Visao

> VOLTAR
OK: /Palco

> ONDE
/Palco

> ESTATISTICAS
pendentes=2, atendidos=0, por_categoria={VIP:1, INTEIRA:1}, espera_media=0.0

> SAIR
```

---

## Decisões de implementação (detalhes importantes)
- **Fila com `deque`**: escolhido pela eficiência nas operações de enfileirar/desenfileirar e por ser requerido pelo enunciado.  
- **Prioridade**: implementada com três `deque`s internos — ao listar ou atender, respeita a ordem VIP → INTEIRA → MEIA, mantendo ordem de chegada dentro de cada fila.  
- **IDs sequenciais**: cada ingresso recebe um `id` único incremental (inteiro).  
- **Tempo lógico**: utilizamos um relógio lógico que incrementa 1 unidade a cada `ENTRAR`; o tempo de espera é calculado como `inicio_atendimento - chegada`.  
- **Undo/Redo**: cada ação que altera estado grava uma operação inversa simplificada no histórico para permitir desfazer; ações de desfazer empilham as operações no redo.  
- **Modularização**: separação por responsabilidades (`fila.py`, `pilha.py`, `ingressos.py`, `roteiro.py`, `terminal.py`) para facilitar testes e manutenção.  
- **Tratamento de erros**: entradas inválidas são tratadas com mensagens claras e sem encerrar o programa.

---

## Testes e Demonstrações
Inclua no arquivo `RELATORIO.pdf` prints de terminal que demonstrem:
- Compras de ingressos (diferentes categorias).  
- Alternância de modo (PADRAO/PRIORIDADE).  
- Atendimentos (`ENTRAR`) e desfazer/refazer.  
- Navegação com `IR`, `VOLTAR`, `AVANCAR` e `ONDE`.  
- Mensagens de erro para comandos inválidos.  

---

## Melhorias futuras
- Persistência do estado (salvar/carregar JSON).  
- Comando `MAPA` com visualização textual do percurso do visitante.  
- Interface gráfica simples (Tkinter) e testes unitários automatizados.

---

## Observações finais
Este README foi revisado e organizado a partir da versão enviada por vocês para garantir clareza, exemplos e instruções de execução.  
(Referência: README enviado pelo grupo).