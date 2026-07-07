# Relatório Técnico — Teste de Carga JMeter

## 1. Identificação

| Campo | Valor |
|---|---|
| Plano de teste | [`test-plan/immigration-api-load-test.jmx`](../test-plan/immigration-api-load-test.jmx) |
| Ferramenta | Apache JMeter 5.6.3, modo non-GUI, JVM OpenJDK 11 |
| Data/hora | 07/07/2026, 19:45:24 → 19:45:44 (BRT) — duração 20,4s |
| Cenário | 25 threads · ramp-up 10s · 2 loops · 350 amostras |
| Alvo | Mock local `mock-api/app.py` (`http://localhost:8099`) |
| Resultado bruto | [`results/results.jtl`](../results/results.jtl) |
| Dashboard | [`results/dashboard/index.html`](../results/dashboard/index.html) |

## 2. Configuração de execução

```bash
python3 mock-api/app.py 8099 &          # sobe o ambiente simulado
jmeter -n -t test-plan/immigration-api-load-test.jmx \
  -Jthreads=25 -Jrampup=10 -Jloops=2 \
  -l results/results.jtl -j results/jmeter.log
jmeter -g results/results.jtl -o results/dashboard   # dashboard HTML
```

## 3. Aggregate Report

| Label | # Samples | Average | Median | 90% Line | 95% Line | 99% Line | Min | Max | Error % | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 - Registro | 50 | 895 | 919 | 1158 | 1260 | 1685 | 264 | 1685 | 0,00% | 3,20/s |
| 02 - Alteracao de Prazo | 50 | 556 | 542 | 757 | 847 | 932 | 252 | 932 | 0,00% | 3,22/s |
| 03 - Autorizacao de Residencia | 50 | 631 | 588 | 1015 | 1237 | 1349 | 212 | 1349 | 0,00% | 3,14/s |
| 04 - Segunda via de CRNM | 50 | 629 | 605 | 977 | 1066 | 1105 | 192 | 1105 | 0,00% | 3,06/s |
| 05 - Substituicao de CRNM | 50 | 651 | 594 | 1019 | 1075 | 1163 | 202 | 1163 | 0,00% | 2,97/s |
| 06 - Solicitar Alteracao de Endereco | 50 | 686 | 714 | 1220 | 1285 | 1465 | 1 | 1465 | **4,00%** | 2,91/s |
| 07 - Recadastramento Extemporaneo | 50 | 849 | 874 | 1242 | 1300 | 1355 | 262 | 1355 | 0,00% | 2,99/s |
| **TOTAL** | **350** | **700** | **689** | **1125** | **1228** | **1355** | **1** | **1685** | **0,57%** | **17,15/s** |

Versões CSV: [`aggregate-report.csv`](../results/aggregate-report.csv) · [`summary-report.csv`](../results/summary-report.csv)

## 4. Análise

### 4.1 Tempo de resposta

Os fluxos **01 - Registro** (média 895 ms) e **07 - Recadastramento Extemporâneo** (849 ms) são os mais lentos, coerente com o processamento de payloads com documentos anexos. Todos os percentis 99 ficaram abaixo de 1,7s; não houve degradação progressiva ao longo da rampa (ver gráfico *Response Times Over Time* no dashboard), indicando ausência de saturação no volume testado.

### 4.2 Erros

2 falhas em 350 amostras (0,57%), **ambas HTTP 503 no fluxo 06**, com tempo de resposta de 1–2 ms e corpo de 226 bytes — resposta imediata característica de rejeição por proxy/balanceador, não de timeout do serviço. O `Min = 1 ms` do fluxo 06 na tabela é artefato dessas falhas rápidas.

### 4.3 Throughput

Vazão global de 17,15 req/s com 25 VUs, distribuída de forma homogênea entre as operações (2,9–3,2 req/s por fluxo), sem indício de fila ou contenção.

## 5. Defeito identificado

HTTP 503 intermitente em `POST /api/v1/alteracao-endereco` — taxa observada de 4% sob carga (2/50). Registro completo, evidências e recomendações em [`bug-report.md`](bug-report.md).

## 6. Limitações

Resultados obtidos em ambiente simulado com modelo de latência derivado do comportamento observado em homologação. Servem para validar o pipeline de teste (plano, execução, relatórios) e a reprodução do defeito; **não substituem** medições no ambiente real com autenticação e payloads completos.

## 7. Próximos passos

Rodadas de 50/100/200 VUs (parâmetros já suportados pelo `.jmx`), teste soak de 1h com 50 VUs, integração em pipeline CI (GitHub Actions) e correlação com métricas de backend (APM) no ambiente real.
