#!/usr/bin/env python3

import csv
import math
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ARQ = sys.argv[1] if len(sys.argv) > 1 else "resultados.csv"
PASTA = os.path.join(os.path.dirname(os.path.abspath(ARQ)), "saida")
FIG = os.path.join(PASTA, "figuras")
TAB = os.path.join(PASTA, "tabelas")
os.makedirs(FIG, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

FONTE = "Fonte: resultados experimentais do grupo 7."
POS = ["Inicio", "25%", "Centro", "75%", "Final"]
AUSENTES = ["Ausente_menor", "Ausente_meio", "Ausente_maior"]
N_OBRIG = [100000, 200000, 300000]   # tamanhos exigidos no enunciado
N_EXTRA = 500000                     # medido apenas para validar as estimativas


def ler_csv(caminho):
    linhas = [l for l in open(caminho, encoding="utf-8") if not l.startswith("#")]
    return list(csv.DictReader(linhas))


def f(x):
    return float(x) if x not in ("", None) else None


dados = ler_csv(ARQ)
ger = {int(r["n"]): r for r in dados if r["tipo"] == "GERACAO"}
ord_ = {int(r["n"]): r for r in dados if r["tipo"] == "ORDENACAO"}
busca = {(int(r["n"]), r["posicao"]): r for r in dados if r["tipo"] == "BUSCA"}
tamanhos = sorted(ger)
obrig = [n for n in tamanhos if n in N_OBRIG]


def media_ger(n):
    return f(ger[n]["tempo_sequencial_s"])


def media_ord(n):
    return f(ord_[n]["tempo_sequencial_s"])


def t_seq(n, p):
    return f(busca[(n, p)]["tempo_sequencial_s"])


def t_bin(n, p):
    return f(busca[(n, p)]["tempo_binaria_s"])


def c_seq(n, p):
    return int(busca[(n, p)]["comparacoes_sequencial"])


def c_bin(n, p):
    return int(busca[(n, p)]["comparacoes_binaria"])


def salvar_fig(nome):
    plt.figtext(0.01, 0.005, FONTE, fontsize=8, color="dimgray")
    plt.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig(os.path.join(FIG, nome), dpi=200)
    plt.close()


def tsv(nome, cab, linhas):
    with open(os.path.join(TAB, nome), "w", encoding="utf-8") as fh:
        fh.write("\t".join(cab) + "\n")
        for l in linhas:
            fh.write("\t".join(str(x) for x in l) + "\n")



def ajuste(xs, ys):
    return sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)


a_ger = ajuste(obrig, [media_ger(n) for n in obrig])
b_ord = ajuste([n * math.log2(n) for n in obrig], [media_ord(n) for n in obrig])
est_ger = lambda n: a_ger * n
est_ord = lambda n: b_ord * n * math.log2(n)


tsv("tabela2_geracao.tsv",
    ["N", "1a (s)", "2a (s)", "3a (s)", "4a (s)", "Media (s)"],
    [[n] + [f"{f(ger[n]['execucao%d_s' % k]):.6f}" for k in range(1, 5)] + [f"{media_ger(n):.6f}"]
     for n in tamanhos])
tsv("tabela3_ordenacao.tsv",
    ["N", "1a (s)", "2a (s)", "3a (s)", "4a (s)", "Media (s)", "Ordenado"],
    [[n] + [f"{f(ord_[n]['execucao%d_s' % k]):.6f}" for k in range(1, 5)]
     + [f"{media_ord(n):.6f}", "Sim" if ord_[n]["ordenado"] == "1" else "NAO"] for n in tamanhos])


linhas4 = []
for n in obrig:
    for p in POS:
        r = busca[(n, p)]
        linhas4.append([n, p, r["chave"], r["indice_sequencial"], r["indice_binario"],
                        f"{t_seq(n, p) * 1e6:.3f}", f"{t_bin(n, p) * 1e9:.0f}",
                        c_seq(n, p), c_bin(n, p)])
tsv("tabela4_buscas_existentes.tsv",
    ["N", "Posicao", "Chave", "Indice seq.", "Indice bin.", "T seq. (us)", "T bin. (ns)",
     "Comp. seq.", "Comp. bin."], linhas4)


linhas5 = []
for n in obrig:
    for p in AUSENTES:
        if (n, p) in busca:
            r = busca[(n, p)]
            linhas5.append([n, p.replace("_", " "), r["chave"], r["indice_sequencial"],
                            r["indice_binario"], c_seq(n, p), c_bin(n, p),
                            f"{t_seq(n, p) * 1e6:.3f}", f"{t_bin(n, p) * 1e9:.0f}"])
tsv("tabela5_buscas_ausentes.tsv",
    ["N", "Chave ausente", "Valor", "Indice seq.", "Indice bin.", "Comp. seq.", "Comp. bin.",
     "T seq. (us)", "T bin. (ns)"], linhas5)


linhas6 = []
for n in [100000, 200000, 300000, 500000]:
    teor = math.ceil(math.log2(n))
    if n in tamanhos:
        obs = max(c_bin(n, p) for p in POS + AUSENTES if (n, p) in busca)
        linhas6.append([n, teor, obs])
    else:
        linhas6.append([n, teor, "nao medido"])
tsv("tabela6_limite_teorico.tsv", ["N", "ceil(log2 N)", "Comparacoes maximas observadas"], linhas6)


linhas7 = []
resumo = []
for n in obrig:
    econ = sum(t_seq(n, p) - t_bin(n, p) for p in POS) / len(POS)
    econ_c = t_seq(n, "Centro") - t_bin(n, "Centro")
    linhas7.append([n, f"{media_ord(n):.6f}", f"{econ * 1e6:.2f}",
                    math.ceil(media_ord(n) / econ), f"{econ_c * 1e6:.2f}",
                    math.ceil(media_ord(n) / econ_c)])
tsv("tabela7_ponto_de_equilibrio.tsv",
    ["N", "Tempo de ordenacao (s)", "Economia media por consulta (us) [5 chaves]",
     "Consultas p/ compensar [5 chaves]", "Economia chave central (us)",
     "Consultas p/ compensar [centro]"], linhas7)


cores = {"Inicio": "#1f77b4", "25%": "#ff7f0e", "Centro": "#2ca02c", "75%": "#d62728", "Final": "#9467bd"}
marc = {"Inicio": "o", "25%": "s", "Centro": "^", "75%": "D", "Final": "v"}
tam_marc = {"Inicio": 11, "25%": 9, "Centro": 7, "75%": 5, "Final": 3}


plt.figure(figsize=(7, 4.5))
plt.plot(obrig, [media_ger(n) * 1e3 for n in obrig], "o-", label="Medido (média de 4 execuções)")
xs = [obrig[0], N_EXTRA]
plt.plot(xs, [est_ger(x) * 1e3 for x in xs], "--", color="gray", label="Ajuste linear t = a·N")
if N_EXTRA in ger:
    plt.plot([N_EXTRA], [media_ger(N_EXTRA) * 1e3], "*", ms=12, color="crimson", label="500.000 (medido p/ validar)")
plt.title("Tempo médio de geração dos vetores")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo médio (ms)")
plt.grid(alpha=.3)
plt.legend()
salvar_fig("fig1_geracao.png")


plt.figure(figsize=(7, 4.5))
plt.plot(obrig, [media_ord(n) * 1e3 for n in obrig], "o-", label="Medido (média de 4 execuções)")
xs = list(range(obrig[0], N_EXTRA + 1, 20000))
plt.plot(xs, [est_ord(x) * 1e3 for x in xs], "--", color="gray", label="Ajuste t = b·N·log₂N")
if N_EXTRA in ord_:
    plt.plot([N_EXTRA], [media_ord(N_EXTRA) * 1e3], "*", ms=12, color="crimson", label="500.000 (medido p/ validar)")
plt.title("Tempo médio de ordenação com qsort()")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo médio (ms)")
plt.grid(alpha=.3)
plt.legend()
salvar_fig("fig2_ordenacao.png")


plt.figure(figsize=(7, 4.5))
for p in POS:
    plt.plot(obrig, [t_seq(n, p) * 1e6 for n in obrig], marker=marc[p], color=cores[p], label=p)
plt.yscale("log")
plt.title("Tempo médio da pesquisa sequencial por posição da chave")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo médio por busca (µs, escala log)")
plt.grid(alpha=.3, which="both")
plt.legend(title="Posição")
salvar_fig("fig3_tempo_sequencial.png")


plt.figure(figsize=(7, 4.5))
for p in POS:
    plt.plot(obrig, [t_bin(n, p) * 1e9 for n in obrig], marker=marc[p], color=cores[p], label=p)
plt.title("Tempo médio da pesquisa binária por posição da chave")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo médio por busca (ns)")
plt.grid(alpha=.3)
plt.legend(title="Posição")
salvar_fig("fig4_tempo_binaria.png")


plt.figure(figsize=(7, 4.5))
for p in POS:
    plt.plot(obrig, [c_seq(n, p) for n in obrig], marker=marc[p], color=cores[p], label=p)
plt.yscale("log")
plt.title("Número de comparações — pesquisa sequencial")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Comparações (escala log)")
plt.grid(alpha=.3, which="both")
plt.legend(title="Posição")
salvar_fig("fig5_comparacoes_sequencial.png")


plt.figure(figsize=(7, 4.5))
for p in POS:
    plt.plot(obrig, [c_bin(n, p) for n in obrig], marker=marc[p], ms=tam_marc[p] + 3, color=cores[p],
             ls="none", label=p)
xs = list(range(obrig[0], N_EXTRA + 1, 250))   # passo pequeno => degraus nitidos
plt.plot(xs, [math.ceil(math.log2(x)) for x in xs], "--", color="black", lw=1, label="⌈log₂N⌉ (limite teórico)")
plt.title("Número de comparações — pesquisa binária")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Comparações")
plt.grid(alpha=.3)
plt.legend(title="Posição", fontsize=8)
salvar_fig("fig6_comparacoes_binaria.png")


plt.figure(figsize=(7, 4.5))
plt.plot(obrig, [t_seq(n, "Centro") * 1e6 for n in obrig], "o-", label="Sequencial")
plt.plot(obrig, [t_bin(n, "Centro") * 1e6 for n in obrig], "s-", label="Binária")
plt.yscale("log")
plt.title("Tempo médio por busca — chave no centro")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo médio por busca (µs, escala log)")
plt.grid(alpha=.3, which="both")
plt.legend()
salvar_fig("fig7_tempo_seq_vs_bin_centro.png")


plt.figure(figsize=(7, 4.5))
plt.plot(obrig, [c_seq(n, "Centro") for n in obrig], "o-", label="Sequencial")
plt.plot(obrig, [c_bin(n, "Centro") for n in obrig], "s-", label="Binária")
plt.yscale("log")
plt.title("Número de comparações — chave no centro")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Comparações (escala log)")
plt.grid(alpha=.3, which="both")
plt.legend()
salvar_fig("fig8_comparacoes_seq_vs_bin_centro.png")


plt.figure(figsize=(7, 4.5))
for p in POS[1:] + AUSENTES:
    ys = [t_seq(n, p) / c_seq(n, p) * 1e9 for n in obrig]
    plt.plot(obrig, ys, marker="o", label=p.replace("_", " "))
plt.title("Custo por comparação na pesquisa sequencial (diagnóstico de ruído)")
plt.xlabel("Número de elementos (N)")
plt.ylabel("Tempo por comparação (ns)")
plt.grid(alpha=.3)
plt.legend(fontsize=8)
salvar_fig("fig9_ns_por_comparacao_sequencial.png")


R = []
R.append("RESUMO NUMERICO PARA A DISCUSSAO\n" + "=" * 60)

R.append("\n[Geracao]  ns por elemento (deve ser ~constante se o tempo e linear)")
for n in tamanhos:
    R.append(f"  N={n:>7}: media={media_ger(n) * 1e3:8.3f} ms  -> {media_ger(n) / n * 1e9:6.1f} ns/elemento")
R.append(f"  ajuste t = a*N: a = {a_ger:.3e} s/elemento (usando {obrig})")
R.append(f"  estimativa 500.000: {est_ger(N_EXTRA) * 1e3:.3f} ms" +
         (f" | medido: {media_ger(N_EXTRA) * 1e3:.3f} ms | erro {100 * (est_ger(N_EXTRA) / media_ger(N_EXTRA) - 1):+.1f}%"
          if N_EXTRA in ger else ""))

R.append("\n[Ordenacao]  razoes entre tamanhos: observado x esperado")
base = obrig[0]
for n in obrig[1:] + ([N_EXTRA] if N_EXTRA in ord_ else []):
    obs = media_ord(n) / media_ord(base)
    lin = n / base
    nln = (n * math.log2(n)) / (base * math.log2(base))
    R.append(f"  {base} -> {n}: observado x{obs:.2f} | linear x{lin:.2f} | n log n x{nln:.2f}")
R.append(f"  ajuste t = b*N*log2(N): b = {b_ord:.3e} s")
R.append(f"  estimativa 500.000: {est_ord(N_EXTRA) * 1e3:.3f} ms" +
         (f" | medido: {media_ord(N_EXTRA) * 1e3:.3f} ms | erro {100 * (est_ord(N_EXTRA) / media_ord(N_EXTRA) - 1):+.1f}%"
          if N_EXTRA in ord_ else ""))
disp = []
for n in tamanhos:
    v = [f(ord_[n]["execucao%d_s" % k]) for k in range(1, 5)]
    disp.append(f"N={n}: max/min das 4 execucoes = {max(v) / min(v):.2f}")
R.append("  dispersao: " + " | ".join(disp) + "   (valor >> 1 indica ruido/aquecimento)")

R.append("\n[Busca sequencial]  ns por comparacao (chaves existentes e ausentes)")
for n in obrig:
    partes = [f"{p}={t_seq(n, p) / c_seq(n, p) * 1e9:.2f}" for p in POS[1:] + AUSENTES if (n, p) in busca]
    R.append(f"  N={n}: " + "  ".join(partes))
R.append("  (se ns/comparacao for ~igual entre as chaves, o tempo e proporcional ao no de comparacoes)")

R.append("\n[Crescimento do tempo da sequencial: chave Final]")
for n in obrig[1:]:
    R.append(f"  {obrig[0]} -> {n}: observado x{t_seq(n, 'Final') / t_seq(obrig[0], 'Final'):.2f} | esperado x{n / obrig[0]:.2f}")

R.append("\n[Busca binaria]  comparacoes maximas e tempo")
for n in obrig + ([N_EXTRA] if N_EXTRA in ger else []):
    mx = max(c_bin(n, p) for p in POS + AUSENTES if (n, p) in busca)
    R.append(f"  N={n}: max comparacoes observado={mx} | ceil(log2 N)={math.ceil(math.log2(n))}")

R.append("\n[Dispersao das rodadas de tempo (max/min) — quanto maior, mais ruidosa a medida]")
for n in obrig:
    ruins = []
    for p in POS + AUSENTES:
        if (n, p) not in busca:
            continue
        r = busca[(n, p)]
        smin, smax = f(r["seq_min_s"]), f(r["seq_max_s"])
        bmin, bmax = f(r["bin_min_s"]), f(r["bin_max_s"])
        if smin and smin > 0 and smax / smin > 1.3:
            ruins.append(f"{p} seq x{smax / smin:.2f}")
        if bmin and bmin > 0 and bmax / bmin > 1.3:
            ruins.append(f"{p} bin x{bmax / bmin:.2f}")
    R.append(f"  N={n}: " + (", ".join(ruins) if ruins else "todas as medidas com max/min <= 1,3"))

R.append("\n[Ponto de equilibrio: consultas necessarias para compensar a ordenacao]")
for l in linhas7:
    R.append(f"  N={l[0]}: ordenar={l[1]} s | economia media={l[2]} us/consulta -> {l[3]} consultas "
             f"| (so chave central: {l[5]})")

ev = os.path.join(os.path.dirname(os.path.abspath(ARQ)), "evidencias.txt")
if os.path.exists(ev):
    txt = open(ev, encoding="utf-8").read()
    R.append("\n[Valores repetidos nos vetores ordenados (de evidencias.txt)]")
    for m in re.finditer(r"=== n = (\d+) ===.*?pares adjacentes com valores repetidos: (\d+)", txt, re.S):
        R.append(f"  N={m.group(1)}: {m.group(2)} pares adjacentes iguais")
    R.append("  Chaves repetidas entre as 5 testadas: " +
             str(len(re.findall(r"chave repetida no vetor", txt))) + " (0 => nenhuma chave testada tem duplicata)")
    R.append("  " + [l for l in txt.splitlines() if l.startswith("RESULTADO GERAL")][0])

open(os.path.join(PASTA, "resumo_analise.txt"), "w", encoding="utf-8").write("\n".join(R) + "\n")
print("\n".join(R))
print(f"\nFiguras em: {FIG}\nTabelas em: {TAB}\nResumo em: {os.path.join(PASTA, 'resumo_analise.txt')}")
