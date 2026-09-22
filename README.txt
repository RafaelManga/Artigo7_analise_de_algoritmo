# Artigo 7 — Comparação entre Algoritmos (pesquisa sequencial x pesquisa binária)

Disciplina: Análise de Algoritmos — UCB — 1º semestre de 2026
Integrantes: Rafael Mangabeira Souza, Paulo Miguel Rodrigues de Jesus Braga, Marcos Antônio Turisco Alves

## Arquivos

* `atividade_algoritmos.c`     — código-fonte completo em C.
* `resultados.csv`             — dados experimentais usados no artigo.
* `evidencias.txt`             — evidências da ordenação e validação das buscas.
* `gerar_graficos_tabelas.py`  — gera figuras, tabelas e resumo numérico a partir do CSV.
* `VALIDACAO.txt`              — resumo da validação da entrega.
* `README.txt`                 — este arquivo.

## Configuração do experimento

* Semente: 306 (três últimos dígitos da matrícula 24101306); `srand(306)` é chamado antes de gerar cada vetor.
* Tamanhos: 100.000, 200.000 e 300.000 elementos (500.000 apenas para validar as estimativas).
* Ordenação: `qsort()` da biblioteca padrão (glibc; merge sort nas versões testadas).
* Repetições por rodada de busca (R): 1.000. Rodadas medidas: 15 (+1 de aquecimento descartada).
  O tempo registrado de cada busca é a MEDIANA das rodadas (T_médio = T_total / R em cada rodada);
  mínimo e máximo das rodadas também são gravados.
* Geração e ordenação: 1 execução de aquecimento descartada + 4 execuções medidas (média).
* Unidade de tempo: segundos (`clock()`; resolução ≈ 1 µs por rodada, ou seja ≈ 1 ns por busca com R = 1.000).
* Chaves: início, 25%, centro, 75%, final (existentes) e três ausentes (menor que todos, no meio, maior que todos).
* Critério de comparação: cada avaliação de `v[i] == chave` conta 1 comparação
  (na binária, um elemento central por iteração). O contador fica dentro das funções cronometradas.
* Ambiente: preencher com o registrado no artigo (SO, processador, memória, GCC, glibc — `ldd --version`).

## Compilar e executar

Linux:

    gcc -std=c11 -O2 -Wall -Wextra -pedantic atividade_algoritmos.c -o atividade_algoritmos
    ./atividade_algoritmos

Windows (MinGW-w64):

    gcc -std=c11 -O2 -Wall -Wextra -pedantic atividade_algoritmos.c -o atividade_algoritmos.exe
    .\atividade_algoritmos.exe

O programa grava `resultados.csv` e `evidencias.txt` na pasta atual (leva 1 a 3 minutos).
Antes de executar: feche outros programas, ligue o notebook na tomada e use o modo de desempenho.

## Gráficos e tabelas

    pip install matplotlib
    python3 gerar_graficos_tabelas.py resultados.csv

Cria a pasta `saida/` com `figuras/` (PNG), `tabelas/` (TSV) e `resumo_analise.txt`.

## Validação

* `evidencias.txt` mostra, para cada tamanho: primeiros/últimos elementos antes e depois da ordenação,
  quantidade de posições fora de ordem (antes > 0, depois = 0), valores repetidos e a validação de cada busca
  (v[índice] == chave, sequencial = 1ª ocorrência, ausentes retornam -1). A última linha deve ser
  `RESULTADO GERAL: TODAS AS VALIDACOES OK`.
* `grep "^ORDENACAO" resultados.csv` deve mostrar `ordenado=1` (campo 13).
* Cada tamanho gera 8 registros BUSCA (5 existentes + 3 ausentes): 4 tamanhos x 8 = 32 registros.

## Observação sobre os tempos

Os resultados determinísticos (chaves, índices e contagens de comparações) se repetem em qualquer execução com a mesma semente.
Os tempos dependem do computador, do sistema operacional e das condições de execução.
