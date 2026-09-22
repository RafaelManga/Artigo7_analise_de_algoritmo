# Guia passo a passo — corrigindo o Artigo 7

Ordem importante: **primeiro os dados novos (Passos 1–3), depois os textos (Passo 4)**, porque vários textos citam números.
Onde aparecer `[ ]`, copie o valor de `saida/resumo_analise.txt` ou das tabelas geradas.

---

## Passo 1 — Rodar o programa novo no notebook do grupo

Use o **mesmo notebook** do primeiro experimento (i3-8130U), para o ambiente registrado continuar valendo.

1. Feche navegador e outros programas, ligue na tomada, modo "desempenho".
2. Na pasta com `atividade_algoritmos.c`:
   ```bash
   gcc -std=c11 -O2 -Wall -Wextra -pedantic atividade_algoritmos.c -o atividade_algoritmos
   ./atividade_algoritmos
   ```
   Não pode aparecer nenhum warning. Leva 1 a 3 minutos e mostra "Concluido. Validacoes: OK".
3. Confira a última linha de `evidencias.txt`: `RESULTADO GERAL: TODAS AS VALIDACOES OK`.
4. Anote a versão da glibc (vai para a metodologia): `ldd --version | head -1`
5. Gere figuras e tabelas:
   ```bash
   pip install matplotlib
   python3 gerar_graficos_tabelas.py resultados.csv
   ```
6. Abra `saida/resumo_analise.txt`. **Se quiser, me mande esse arquivo e o `evidencias.txt`** que eu escrevo as seções 4.1–4.5, 6 e 7 já com os seus números.

O que mudou no código (para citar na metodologia): aquecimento descartado antes de medir; tempo de busca = mediana de 15 rodadas; `srand(306)` antes de cada vetor; três chaves ausentes; vetor de 500.000 só para validar estimativas; arquivo de evidências.

## Passo 2 — Atualizar os arquivos entregues

Substitua no zip/GitHub: `atividade_algoritmos.c`, `README.txt`, `VALIDACAO.txt`, `resultados.csv` (novo) e adicione `evidencias.txt` e `gerar_graficos_tabelas.py`.
No `README.txt`, preencha a linha "Ambiente" com SO, processador, memória, GCC e glibc.

## Passo 3 — Trocar tabelas e figuras do PDF

Os números das figuras/tabelas são os mesmos do artigo. Cole as tabelas como **tabelas de verdade** (não print): abra o `.tsv` no Excel, copie, cole no Word/Docs.

| No artigo | Arquivo novo | Observação |
|---|---|---|
| Tabela 2 (geração) | `tabela2_geracao.tsv` | **Sem coluna "Ordenado"** (vetor gerado não está ordenado) |
| Tabela 3 (ordenação) | `tabela3_ordenacao.tsv` | mantém "Ordenado" |
| Tabela 4 (buscas existentes) | `tabela4_buscas_existentes.tsv` | tempo seq. em µs, bin. em ns |
| Tabela 5 (chave ausente) | `tabela5_buscas_ausentes.tsv` | agora 3 ausentes por tamanho |
| Tabela 6 (limite teórico) | `tabela6_limite_teorico.tsv` | 500.000 agora **medido** |
| **Tabela 7 (nova)** | `tabela7_ponto_de_equilibrio.tsv` | custo da ordenação x consultas |
| Figuras 1–8 | `fig1` … `fig8` | escala log nas Figs. 3, 5, 7, 8; teórico na Fig. 6 |
| **Figura 9 (nova)** | `fig9_ns_por_comparacao_sequencial.png` | mostra se há ruído nas medidas |

Legenda sugerida para a Figura 6 (as séries se sobrepõem): *"Figura 6 — Número de comparações da pesquisa binária. Os marcadores de Início, 25%, Centro e 75% coincidem, pois essas chaves exigiram o mesmo número de comparações; a linha tracejada é ⌈log₂N⌉. Fonte: resultados experimentais do grupo 7."* (confirme na tabela se isso vale nos seus dados).

Apague a página quase vazia do "Cálculo da estimativa": o cálculo novo vai no texto (Passo 4.4).

---

## Passo 4 — Textos para colar

### 4.1 Título e resumo
**Título:** *Comparação experimental entre pesquisa sequencial e pesquisa binária em vetores de inteiros*

**Resumo (modelo, complete os `[ ]`):**
> Este artigo compara experimentalmente as pesquisas sequencial e binária em vetores de inteiros pseudoaleatórios com 100.000, 200.000 e 300.000 elementos, gerados com a semente 306 (três últimos dígitos da matrícula 24101306) e ordenados com `qsort()`. Foram pesquisadas chaves nas posições inicial, 25%, central, 75% e final, além de chaves ausentes; cada tempo corresponde à mediana de 15 rodadas de 1.000 repetições, e as comparações foram contadas em todas as buscas. A pesquisa sequencial realizou de 1 a N comparações e teve tempo proporcional à posição da chave (≈ [0,69] ns por comparação), enquanto a binária realizou no máximo 17, 18 e 19 comparações, coerente com ⌈log₂N⌉. A ordenação custou [ ] ms para 300.000 elementos e é compensada a partir de cerca de [ ] consultas. Conclui-se que a pesquisa binária é vantajosa para vetores consultados repetidamente, e a sequencial, para poucas consultas ou dados não ordenados.

Palavras-chave: pode manter as atuais (5 termos).

### 4.2 Fundamentação teórica — substituir a seção 2.3 por estas duas

**2.3 Ordenação**
> A pesquisa binária exige o vetor ordenado. A ordenação por comparações tem custo mínimo Ω(n log n) no pior caso (CORMEN et al., 2022), e algoritmos como merge sort e heap sort atingem O(n log n). Neste trabalho foi utilizada a função `qsort()` da biblioteca padrão de C, que na glibc `[versão]` é implementada com merge sort e memória auxiliar `[confirmar]`. Assim, espera-se que o tempo de ordenação cresça mais que linearmente: ao passar de N₁ para N₂ elementos, a razão esperada é (N₂ log N₂)/(N₁ log N₁) — por exemplo, ×2,12 de 100.000 para 200.000 e ×3,29 para 300.000.

**2.4 Complexidade assintótica e medição de desempenho**
> A complexidade assintótica descreve como o custo de um algoritmo cresce com o tamanho da entrada, desprezando constantes: f(n) = O(g(n)) se existem c > 0 e n₀ tais que f(n) ≤ c·g(n) para todo n ≥ n₀ (CORMEN et al., 2022). A pesquisa sequencial é O(1) no melhor caso e O(n) no pior; a binária é O(log n) no pior caso, pois cada comparação descarta metade do intervalo, o que dá no máximo ⌊log₂n⌋ + 1 ≈ ⌈log₂n⌉ comparações (KNUTH, 1998). A análise assintótica prevê tendências, não tempos absolutos: o tempo real depende de constantes, do hardware, da hierarquia de memória, do compilador e do sistema operacional. Por isso, a medição exige cuidados: descartar execuções de aquecimento, repetir a operação para superar a resolução do relógio e resumir várias rodadas por uma estatística robusta, como a mediana. Além do tempo, a contagem de comparações é uma medida independente da máquina.

### 4.3 Metodologia — acrescentar
> **Geração.** `srand(306)` foi chamado imediatamente antes da geração de cada vetor, de modo que os vetores são reprodutíveis e o vetor de 100.000 elementos é o prefixo dos maiores. **Ordenação.** `qsort()` da glibc `[versão]`; o tempo é a média de 4 execuções, cada uma sobre uma cópia do vetor, precedidas de uma execução de aquecimento descartada. **Busca.** Cada chave foi pesquisada 1.000 vezes por rodada (R = 1.000, igual nas duas pesquisas); foram medidas 15 rodadas, após uma de aquecimento descartada, e adotou-se a mediana de T_total/R. O relógio `clock()` tem resolução de ≈ 1 µs, ou seja, ≈ 1 ns por busca com R = 1.000; tempos de poucos nanossegundos (como o da chave inicial na sequencial) estão no limite dessa resolução. **Chaves ausentes.** Foram usadas três: `INT_MIN` (menor que todos os elementos), um valor entre elementos do centro do vetor e `INT_MAX` (maior que todos). **Validação.** Para cada busca, verificou-se v[índice] == chave e, para as ausentes, retorno −1; a ordenação foi verificada por v[i−1] ≤ v[i] em todas as posições (evidências em `evidencias.txt`).

Limitações a citar (uma frase cada): repetir a mesma chave 1.000× mantém cache e preditor de desvios "aquecidos", então os tempos absolutos são otimistas; o contador de comparações está dentro das funções cronometradas; os experimentos foram feitos em um único computador.

### 4.4 Resultados — modelos de parágrafo

**Geração e estimativa para 500.000** (substitui o texto e a imagem do cálculo):
> O tempo médio de geração foi [ ] ms, [ ] ms e [ ] ms para 100.000, 200.000 e 300.000 elementos, ou seja, cerca de [18] ns por elemento em todos os tamanhos, o que confirma o comportamento linear. Ajustando t = a·N por mínimos quadrados, obteve-se a = [ ] s/elemento, e a estimativa para 500.000 elementos é a·500.000 = [ ] ms. Como verificação, o vetor de 500.000 elementos foi de fato gerado e o tempo medido foi [ ] ms (diferença de [ ]%).

*(Se os tempos da geração ainda vierem "tortos" no seu computador, diga isso e explique: variação de frequência da CPU e efeitos de memória em execuções curtas.)*

**Ordenação** (responda a pergunta do enunciado com sim/não):
> A média de ordenação foi [ ] s, [ ] s e [ ] s. De 100.000 para 300.000 elementos o tempo multiplicou por [ ]; uma função linear preveria ×3,00 e N log N preveria ×3,29. O tempo, portanto, [não] cresceu proporcionalmente ao tamanho: [cresceu ligeiramente mais que linearmente, como esperado para N log N]. Ajustando t = b·N·log₂N, a estimativa para 500.000 elementos é [ ] ms, contra [ ] ms medidos.

*(Se sobrar um outlier na 1ª execução mesmo com o aquecimento, mencione-o em vez de escondê-lo. Um resultado explicado vale mais que um resultado "bonito".)*

**Buscas existentes (Tabela 4, Figuras 3–8)** — sempre cite tabela/figura pelo número:
> A Tabela 4 mostra que, na pesquisa sequencial, o número de comparações é igual à posição da chave mais um (1, 25.001, 50.001, 75.001 e 100.000 para N = 100.000), e o tempo acompanha essa contagem: [0,69] ns por comparação, praticamente constante entre chaves e tamanhos (Figura 9). Na binária, o número de comparações ficou entre 16 e 19 (Figuras 5 e 6), independentemente da posição, e o tempo entre [ ] e [ ] ns (Figura 4). A Figura 7 mostra que, para a chave central, a diferença de tempo é de ≈ [3] ordens de grandeza (escala logarítmica).

**Chaves ausentes (Tabela 5):**
> Na chave ausente a sequencial percorreu todo o vetor (N comparações, igual ao caso da chave final), e a binária encerrou com [16–17], [17–18] e [18–19] comparações para 100.000, 200.000 e 300.000 elementos. A chave `INT_MIN` sempre leva a busca para a esquerda; por isso foram testadas também chaves ausentes no meio e no maior valor.

**Limite teórico (Tabela 6) — a explicação que o enunciado pede:**
> A cada comparação a pesquisa binária descarta metade do intervalo; portanto, dobrar o tamanho do vetor acrescenta apenas uma comparação (17 → 18 de 100.000 para 200.000) e multiplicar por 5 acrescenta duas (17 → 19 de 100.000 para 500.000). O crescimento é logarítmico, não proporcional a N. O máximo observado coincidiu com ⌈log₂N⌉ em todos os tamanhos, inclusive 500.000 (19).

### 4.5 Discussão — trechos que precisam substituir os antigos

**Anomalias de tempo.** Abra `resumo_analise.txt`, seções "ns por comparação" e "Dispersão".
- Se ns/comparação for ≈ constante entre chaves: escreva isso — é a evidência de que o tempo é proporcional às comparações.
- Se ainda houver pontos fora do padrão (max/min > 1,3), cite cada um pelo nome e explique: variação de frequência da CPU, interrupções do sistema, cache. Não escreva só "condições do ambiente".
- Para a chave inicial da sequencial (1 comparação), diga que o tempo está no limite de resolução do relógio.

**Custo da ordenação (questão 10) — substituir a resposta:**
> O custo de ordenar é compensado quando o número de consultas supera a razão entre o tempo de ordenação e a economia por consulta. Com os dados da Tabela 7, ordenar 100.000, 200.000 e 300.000 elementos custa [ ], [ ] e [ ] s, e cada consulta binária economiza em média [ ], [ ] e [ ] µs em relação à sequencial; logo, a ordenação se paga a partir de ≈ [ ], [ ] e [ ] consultas, respectivamente. Abaixo disso (ou com dados que mudam a cada consulta, exigindo reordenar), a sequencial é mais econômica no total.

**Valores repetidos (questão 11) — substituir; o texto antigo estava errado:**
> Os vetores possuem valores repetidos: após a ordenação há [1], [7], [18] e [58] pares adjacentes iguais nos vetores de 100.000, 200.000, 300.000 e 500.000 elementos (`evidencias.txt`), compatível com o esperado pelo paradoxo do aniversário, ≈ N²/(2·2³¹) (2,3; 9,3; 20,9 e 58). Nenhuma das cinco chaves testadas em cada vetor é repetida, e por isso as duas funções retornaram o mesmo índice. Se a chave tivesse repetições, a sequencial retornaria sempre a primeira ocorrência (varre da esquerda para a direita), enquanto a binária retornaria a primeira que o intervalo central atingisse, sem garantia de ser a primeira.

*(Confira os números `[1] [7] [18] [58]` no seu `evidencias.txt`; devem ser iguais, pois `rand()` da glibc é determinístico.)*

**Questão 6 (linear?)** — dê números: *"Na chave final, o tempo foi de [ ] µs, [ ] µs e [ ] µs (×[ ] e ×[ ] em relação a 100.000, contra ×2 e ×3 esperados)."*

**Questão 8 (teoria x medição)** — cite o que **de fato** apareceu (constantes, resolução de 1 ns, aquecimento, mesma chave repetida), com números.

### 4.6 Referências e citações

Ordem alfabética (ABNT):
```
CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. Introduction to Algorithms. 4. ed. Cambridge: MIT Press, 2022.
ISO/IEC. ISO/IEC 9899:2018 — Information technology — Programming languages — C. Geneva: ISO, 2018.
KERNIGHAN, B. W.; RITCHIE, D. M. The C Programming Language. 2. ed. Englewood Cliffs: Prentice Hall, 1988.
KNUTH, D. E. The Art of Computer Programming, Volume 3: Sorting and Searching. 2. ed. Reading: Addison-Wesley, 1998.
RAFAELMANGA. Artigo7_analise_de_algoritmo. GitHub, 2026. Disponível em: https://github.com/RafaelManga/Artigo7_analise_de_algoritmo. Acesso em: [data].
```
Cada referência precisa ser **citada no texto**: CORMEN et al. (2022) e KNUTH (1998) na fundamentação; ISO/IEC (2018) ao falar de `qsort`, `rand`, `clock`; KERNIGHAN e RITCHIE (1988) ao citar as funções da biblioteca padrão. Se alguma não for citada, retire da lista.

### 4.7 Localizar e substituir (typos)

| Onde | Trocar | Por |
|---|---|---|
| Resumo | `306(UC24101306)` | `306 (três últimos dígitos da matrícula 24101306)` |
| Introdução | `mas requer os dados estejam ordenados` | `mas requer que os dados estejam ordenados` |
| Introdução | `Já a pesquisa binária` | `já a pesquisa binária` (após vírgula) |
| Introdução | `contar comparações ,` | `contar comparações,` |
| Resumo | `Foram avaliados cinco posições` | `Foram avaliadas cinco posições` |
| 3.2 | `7,8 GIB disponíveis` | `7,8 GiB` (informe memória total) |
| 4.3 | `A coluna de chave contém agora o valor…` | `A coluna Chave contém o valor inteiro pesquisado…` |
| Todas | "Fonte : " | "Fonte: " |

---

## Passo 5 — Checklist antes de reenviar

- [ ] `evidencias.txt` termina com `TODAS AS VALIDACOES OK`
- [ ] Todas as tabelas e figuras têm número, título, unidade, fonte **e são citadas no texto**
- [ ] Tabelas 4, 5, 6, 7 são tabelas reais (sem print, sem borda tracejada)
- [ ] Nenhum número do texto contradiz as tabelas novas (releia 4.1, 4.2 e Discussão)
- [ ] Ambiente na metodologia inclui a versão da glibc e o algoritmo de `qsort`
- [ ] Fundamentação tem O/Ω, n log n e medição de desempenho, com citações
- [ ] Questões 6, 8, 10 e 11 respondidas com números
- [ ] Resumo com resultados numéricos
- [ ] Zip com: PDF, `atividade_algoritmos.c`, `resultados.csv`, `evidencias.txt`, `gerar_graficos_tabelas.py`, `README.txt`, `VALIDACAO.txt`
- [ ] Os três integrantes leram e concordam com o reenvio

**E-mail:**
> **Assunto:** Artigo 7 – Grupo 7 – Versão corrigida (substitui o envio anterior)
>
> Prezado professor Marcelo,
> Após revisão, refizemos as medições de tempo (com aquecimento e mediana de 15 rodadas), incluímos evidências de ordenação e validação, e corrigimos a análise de ordenação, de valores repetidos e do custo de ordenação. Pedimos que considere esta versão no lugar da enviada anteriormente. Seguem o artigo em PDF, o código-fonte em C, os dados experimentais e as evidências. Repositório: https://github.com/RafaelManga/Artigo7_analise_de_algoritmo
> Atenciosamente, Grupo 7 — Rafael Mangabeira Souza, Paulo Miguel Rodrigues de Jesus Braga e Marcos Antônio Turisco Alves.

(Lembre de atualizar o GitHub com os arquivos novos antes de enviar.)
