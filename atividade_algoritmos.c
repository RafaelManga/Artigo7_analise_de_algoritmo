/*
 * Artigo 7 - Comparação entre pesquisa sequencial e pesquisa binária
 * Análise de Algoritmos - UCB - 1º semestre de 2026
 *
 * Compilação: gcc -std=c11 -O2 -Wall -Wextra -pedantic atividade_algoritmos.c -o atividade_algoritmos
 * Saídas:     resultados.csv (dados experimentais) e evidencias.txt (ordenação e validação)
 *
 * Critério de contagem: cada avaliação de v[posição] == chave conta 1 comparação
 * (na pesquisa binária, um elemento central por iteração).
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>

#define ERRO (-1)
#define REPETICOES 1000   /* repetições de cada busca em uma rodada (R) */
#define RODADAS 15        /* rodadas medidas, além de 1 de aquecimento */
#define SEMENTE 306       /* três últimos dígitos da matrícula 24101306 */

static volatile long long sum_sink = 0; /* impede o compilador de eliminar as buscas */

typedef struct {
    int indice;
    long long comparacoes;
} ResultadoBusca;

typedef ResultadoBusca (*FuncaoBusca)(const int *, int, int);

/* Pesquisa sequencial: percorre o vetor da esquerda para a direita. */
ResultadoBusca pesquisa_sequencial(const int *v, int n, int chave) {
    ResultadoBusca r = {ERRO, 0};
    for (int i = 0; i < n; ++i) {
        r.comparacoes++;
        if (v[i] == chave) {
            r.indice = i;
            return r;
        }
    }
    return r;
}

/* Pesquisa binária: exige vetor ordenado; descarta metade do intervalo a cada iteração. */
ResultadoBusca pesquisa_binaria(const int *v, int n, int chave) {
    ResultadoBusca r = {ERRO, 0};
    int esquerda = 0, direita = n - 1;
    while (esquerda <= direita) {
        int meio = esquerda + (direita - esquerda) / 2; /* evita overflow */
        r.comparacoes++;
        if (v[meio] == chave) {
            r.indice = meio;
            return r;
        }
        if (v[meio] < chave) esquerda = meio + 1;
        else direita = meio - 1;
    }
    return r;
}

/* Função de comparação exigida pelo qsort(). */
int comparar_ints(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);
}

/* Retorna 1 se o vetor está em ordem crescente. */
int esta_ordenado(const int *v, int n) {
    for (int i = 1; i < n; ++i)
        if (v[i - 1] > v[i]) return 0;
    return 1;
}

/* Conta as posições em que v[i-1] > v[i] (0 significa vetor ordenado). */
long long contar_desordem(const int *v, int n) {
    long long c = 0;
    for (int i = 1; i < n; ++i)
        if (v[i - 1] > v[i]) c++;
    return c;
}

/* Conta pares adjacentes iguais no vetor ordenado (valores repetidos). */
long long contar_repetidos(const int *v, int n) {
    long long c = 0;
    for (int i = 1; i < n; ++i)
        if (v[i] == v[i - 1]) c++;
    return c;
}

/* Retorna 1 se a chave da posição p possui outra ocorrência vizinha. */
int chave_repetida(const int *v, int n, int p) {
    return (p > 0 && v[p] == v[p - 1]) || (p < n - 1 && v[p] == v[p + 1]);
}

/* Gera n números pseudoaleatórios com a semente fixa. */
void gerar_vetor(int *v, int n) {
    srand(SEMENTE);
    for (int i = 0; i < n; ++i) v[i] = rand();
}

/* Ordena um pequeno vetor de tempos (inserção). */
void ordenar_tempos(double *t, int m) {
    for (int i = 1; i < m; ++i) {
        double x = t[i];
        int j = i - 1;
        while (j >= 0 && t[j] > x) {
            t[j + 1] = t[j];
            j--;
        }
        t[j + 1] = x;
    }
}

/* Uma rodada: executa a busca REPETICOES vezes e retorna T_médio = T_total / R (segundos). */
double medir_rodada(FuncaoBusca f, const int *v, int n, int chave) {
    clock_t inicio = clock();
    for (int i = 0; i < REPETICOES; ++i) {
        ResultadoBusca r = f(v, n, chave);
        sum_sink += r.indice;
    }
    clock_t fim = clock();
    return ((double)(fim - inicio) / CLOCKS_PER_SEC) / REPETICOES;
}

/* Descarta 1 rodada de aquecimento, mede RODADAS rodadas e devolve mediana, mínimo e máximo. */
void medir_busca(FuncaoBusca f, const int *v, int n, int chave,
                 double *mediana, double *minimo, double *maximo) {
    double t[RODADAS];
    (void)medir_rodada(f, v, n, chave);
    for (int k = 0; k < RODADAS; ++k) t[k] = medir_rodada(f, v, n, chave);
    ordenar_tempos(t, RODADAS);
    *mediana = t[RODADAS / 2];
    *minimo = t[0];
    *maximo = t[RODADAS - 1];
}

/* Registra em evidencias.txt os 5 primeiros e os 5 últimos elementos. */
void imprimir_pontas(FILE *ev, const char *titulo, const int *v, int n) {
    fprintf(ev, "  %s\n    primeiros 5: ", titulo);
    for (int i = 0; i < 5; ++i) fprintf(ev, "%d ", v[i]);
    fprintf(ev, "\n    ultimos 5:   ");
    for (int i = n - 5; i < n; ++i) fprintf(ev, "%d ", v[i]);
    fprintf(ev, "\n");
}

int main(void) {
    const int tamanhos[] = {100000, 200000, 300000, 500000}; /* 500000: apenas valida as estimativas */
    const int qtd_tamanhos = 4;
    const char *rotulos[] = {"Inicio", "25%", "Centro", "75%", "Final"};
    int tudo_ok = 1;

    FILE *csv = fopen("resultados.csv", "w");
    FILE *ev = fopen("evidencias.txt", "w");
    if (!csv || !ev) {
        fprintf(stderr, "ERRO: não foi possível criar os arquivos de saída\n");
        return EXIT_FAILURE;
    }

    fprintf(csv, "# semente=%d; repeticoes=%d; rodadas=%d (+1 de aquecimento; tempo = mediana); unidade=segundos; "
                 "opcoes=-std=c11 -O2 -Wall -Wextra -pedantic\n", SEMENTE, REPETICOES, RODADAS);
    fprintf(csv, "# comparacao = uma avaliacao de v[i] == chave (um elemento central por iteracao na binaria)\n");
    fprintf(csv, "tipo,n,posicao,chave,indice_sequencial,indice_binario,execucao1_s,execucao2_s,execucao3_s,"
                 "execucao4_s,tempo_sequencial_s,tempo_binaria_s,ordenado,comparacoes_sequencial,"
                 "comparacoes_binaria,seq_min_s,seq_max_s,bin_min_s,bin_max_s\n");
    fprintf(ev, "EVIDENCIAS DA ORDENACAO E DA VALIDACAO DAS BUSCAS\n");
    fprintf(ev, "semente=%d (srand chamado antes de gerar cada vetor)\n\n", SEMENTE);

    for (int ti = 0; ti < qtd_tamanhos; ++ti) {
        int n = tamanhos[ti];
        fprintf(stderr, "Processando n=%d ...\n", n);

        int *v = malloc((size_t)n * sizeof(int));
        int *aux = malloc((size_t)n * sizeof(int)); /* buffer para medir geração e ordenar cópias */
        if (!v || !aux) {
            fprintf(stderr, "ERRO: memória insuficiente\n");
            free(v);
            free(aux);
            return EXIT_FAILURE;
        }

        /* Geração: vetor de teste + 1 execução de aquecimento + 4 medições */
        gerar_vetor(v, n);
        gerar_vetor(aux, n);
        double geracao[4];
        for (int e = 0; e < 4; ++e) {
            srand(SEMENTE);
            clock_t ini = clock();
            for (int i = 0; i < n; ++i) aux[i] = rand();
            clock_t fim = clock();
            geracao[e] = (double)(fim - ini) / CLOCKS_PER_SEC;
        }
        double media_geracao = (geracao[0] + geracao[1] + geracao[2] + geracao[3]) / 4.0;

        fprintf(ev, "=== n = %d ===\n", n);
        imprimir_pontas(ev, "Vetor gerado (antes de ordenar):", v, n);
        fprintf(ev, "  posicoes com v[i-1] > v[i] antes de ordenar: %lld\n", contar_desordem(v, n));

        /* Ordenação: 1 aquecimento + 4 medições, sempre sobre cópias do vetor gerado */
        double ord[4];
        int copias_ok = 1;
        for (int i = 0; i < n; ++i) aux[i] = v[i];
        qsort(aux, (size_t)n, sizeof(int), comparar_ints);
        for (int e = 0; e < 4; ++e) {
            for (int i = 0; i < n; ++i) aux[i] = v[i];
            clock_t ini = clock();
            qsort(aux, (size_t)n, sizeof(int), comparar_ints);
            clock_t fim = clock();
            ord[e] = (double)(fim - ini) / CLOCKS_PER_SEC;
            if (!esta_ordenado(aux, n)) copias_ok = 0;
        }
        double media_ord = (ord[0] + ord[1] + ord[2] + ord[3]) / 4.0;

        qsort(v, (size_t)n, sizeof(int), comparar_ints); /* vetor ordenado usado nas buscas */
        int ordenado = esta_ordenado(v, n) && copias_ok;
        if (!ordenado) tudo_ok = 0;

        imprimir_pontas(ev, "Vetor apos qsort():", v, n);
        fprintf(ev, "  posicoes com v[i-1] > v[i] apos ordenar: %lld  -> ordenado = %s\n",
                contar_desordem(v, n), ordenado ? "SIM" : "NAO");
        fprintf(ev, "  pares adjacentes com valores repetidos: %lld\n", contar_repetidos(v, n));

        fprintf(csv, "GERACAO,%d,,,,,%.9f,%.9f,%.9f,%.9f,%.9f,,,,,,,,\n",
                n, geracao[0], geracao[1], geracao[2], geracao[3], media_geracao);
        fprintf(csv, "ORDENACAO,%d,,,,,%.9f,%.9f,%.9f,%.9f,%.9f,,%d,,,,,,\n",
                n, ord[0], ord[1], ord[2], ord[3], media_ord, ordenado);

        /* Chaves: 5 existentes (0, 25%, 50%, 75%, final) e 3 ausentes */
        int posicoes[5] = {0, n / 4, n / 2, (3 * n) / 4, n - 1};
        int chaves[8];
        const char *nomes[8];
        int existe[8];
        for (int p = 0; p < 5; ++p) {
            chaves[p] = v[posicoes[p]];
            nomes[p] = rotulos[p];
            existe[p] = 1;
        }
        int i_meio = n / 2; /* ausente no meio: primeiro valor v[i]+1 que não aparece no vetor */
        while (i_meio + 1 < n && v[i_meio + 1] <= v[i_meio] + 1) i_meio++;
        chaves[5] = INT_MIN;       nomes[5] = "Ausente_menor"; existe[5] = 0;
        chaves[6] = v[i_meio] + 1; nomes[6] = "Ausente_meio";  existe[6] = 0;
        chaves[7] = INT_MAX;       nomes[7] = "Ausente_maior"; existe[7] = 0;

        fprintf(ev, "  Validacao das buscas:\n");
        for (int k = 0; k < 8; ++k) {
            int chave = chaves[k];
            ResultadoBusca rs = pesquisa_sequencial(v, n, chave);
            ResultadoBusca rb = pesquisa_binaria(v, n, chave);

            /* Validação: existente => v[índice] == chave (sequencial = 1ª ocorrência); ausente => -1 */
            int ok;
            if (existe[k]) {
                ok = rs.indice >= 0 && rb.indice >= 0 &&
                     v[rs.indice] == chave && v[rb.indice] == chave &&
                     (rs.indice == 0 || v[rs.indice - 1] != chave);
            } else {
                ok = (rs.indice == ERRO && rb.indice == ERRO);
            }
            if (!ok) tudo_ok = 0;

            fprintf(ev, "    %-13s chave=%-11d idx_seq=%-7d idx_bin=%-7d comp_seq=%-7lld comp_bin=%-3lld %s%s\n",
                    nomes[k], chave, rs.indice, rb.indice, rs.comparacoes, rb.comparacoes,
                    ok ? "VALIDA" : "FALHA",
                    existe[k] ? (chave_repetida(v, n, posicoes[k]) ? " (chave repetida no vetor)"
                                                                  : " (chave unica no vetor)")
                              : " (chave ausente: ambos devem retornar -1)");

            double ts, ts_min, ts_max, tb, tb_min, tb_max;
            medir_busca(pesquisa_sequencial, v, n, chave, &ts, &ts_min, &ts_max);
            medir_busca(pesquisa_binaria, v, n, chave, &tb, &tb_min, &tb_max);

            fprintf(csv, "BUSCA,%d,%s,%d,%d,%d,,,,,%.9f,%.9f,,%lld,%lld,%.9f,%.9f,%.9f,%.9f\n",
                    n, nomes[k], chave, rs.indice, rb.indice, ts, tb,
                    rs.comparacoes, rb.comparacoes, ts_min, ts_max, tb_min, tb_max);
        }
        fprintf(ev, "\n");

        free(v);
        free(aux);
    }

    fprintf(ev, "RESULTADO GERAL: %s\n", tudo_ok ? "TODAS AS VALIDACOES OK" : "HOUVE FALHAS - VERIFICAR");
    fclose(csv);
    fclose(ev);
    fprintf(stderr, "Concluído. Validações: %s (sum_sink=%lld)\n", tudo_ok ? "OK" : "FALHA", sum_sink);
    return tudo_ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
