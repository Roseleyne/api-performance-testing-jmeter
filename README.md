# API Performance Testing com JMeter — Immigration Services REST API

![JMeter](https://img.shields.io/badge/Apache%20JMeter-5.6.3-D22128?logo=apachejmeter&logoColor=white)
![Tests](https://img.shields.io/badge/amostras-350-blue)
![Errors](https://img.shields.io/badge/erro%20global-0.57%25-yellow)
![Status](https://img.shields.io/badge/veredicto-aprovado%20com%20ressalva-orange)

Projeto de teste de performance com **Apache JMeter** sobre uma API REST de serviços de imigração (sanitizada — sem URLs, dados ou credenciais reais). Inclui plano de teste versionado, execução reprodutível contra ambiente simulado, dashboard HTML, relatórios e documentação completa de QA.

## 📊 Resultados da última execução (07/07/2026)

Cenário: **25 usuários virtuais · ramp-up 10s · 2 loops · 350 amostras**

| Métrica | Resultado |
|---|---:|
| Tempo médio de resposta | 700 ms |
| 90% Line / 95% Line | 1.125 ms / 1.228 ms |
| Throughput | 17,15 req/s |
| Erro global | 0,57% |
| Erro no fluxo "Alteração de Endereço" | **4,00% (HTTP 503)** ⚠️ |

**Veredicto: aprovado com ressalva** — desempenho global dentro do SLA, porém o defeito intermitente HTTP 503 foi reproduzido sob carga. Ver [Bug Report](docs/bug-report.md).

## 📁 Estrutura do repositório

```
├── test-plan/
│   ├── immigration-api-load-test.jmx    # Plano JMeter 5.6.3 parametrizado
│   ├── plano-de-teste.md                # Plano de teste formal (escopo, SLA, riscos)
│   └── sanitized-test-plan-notes.md     # Notas do plano original sanitizado
├── mock-api/
│   └── app.py                           # Ambiente alvo simulado (Python 3, sem dependências)
├── results/
│   ├── dashboard/index.html             # ✅ Dashboard HTML oficial do JMeter
│   ├── aggregate-report.csv|md          # ✅ Aggregate Report
│   ├── summary-report.csv|md            # ✅ Summary Report
│   ├── results.jtl                      # Resultado bruto da execução (sanitizado)
│   └── sample-summary-sanitized.csv     # Baseline histórico (homologação)
├── docs/
│   ├── relatorio-executivo.md           # ✅ Relatório Executivo
│   ├── relatorio-tecnico.md             # ✅ Relatório Técnico
│   ├── bug-report.md                    # ✅ Bug Report (HTTP 503 intermitente)
│   ├── fluxograma.md                    # ✅ Fluxograma (Mermaid)
│   ├── diagrama-arquitetura.md          # ✅ Diagrama de arquitetura (Mermaid)
│   └── test-strategy.md                 # Estratégia de teste
└── scripts/
    └── run-test.sh                      # Execução completa em um comando
```

## 🚀 Como executar

Pré-requisitos: [Apache JMeter 5.6+](https://jmeter.apache.org/download_jmeter.cgi) no PATH e Python 3.

```bash
git clone https://github.com/Roseleyne/api-performance-testing-jmeter.git
cd api-performance-testing-jmeter
./scripts/run-test.sh              # cenário padrão: 25 VUs, ramp-up 10s, 2 loops
./scripts/run-test.sh 50 120 1     # carga média: 50 VUs, ramp-up 120s, 1 loop
```

Ou manualmente:

```bash
python3 mock-api/app.py 8099 &
jmeter -n -t test-plan/immigration-api-load-test.jmx \
  -Jthreads=25 -Jrampup=10 -Jloops=2 \
  -l results/results.jtl -e -o results/dashboard
```

O plano aceita os parâmetros `-Jhost`, `-Jport`, `-Jprotocol`, `-Jthreads`, `-Jrampup` e `-Jloops` — para apontar a outro ambiente, basta trocar host/porta, sem editar o `.jmx`.

## 🔎 Fluxos testados

1. Registro · 2. Alteração de Prazo · 3. Autorização de Residência · 4. Segunda via de CRNM · 5. Substituição de CRNM · 6. Solicitar Alteração de Endereço · 7. Recadastramento Extemporâneo

## 🐞 Defeito documentado

`POST /api/v1/alteracao-endereco` retorna **HTTP 503** de forma intermitente (resposta em 1–2 ms, característica de rejeição por proxy/balanceador). Identificado no baseline, **reproduzido sob carga** com taxa de 4%. Registro completo: [docs/bug-report.md](docs/bug-report.md).

## 🔐 Observações de segurança

Projeto sanitizado para publicação: URLs reais mascaradas, massa de dados 100% fictícia, payloads Base64 removidos, sem tokens/cookies/headers sensíveis. O ambiente alvo é um mock local que replica o contrato da API real.

## 📌 Próximos passos

- [ ] Rodadas de carga média (50 VUs), alta (100 VUs) e stress (200 VUs)
- [ ] Teste soak (50 VUs por 1h)
- [ ] Pipeline CI com GitHub Actions executando o teste a cada push
- [ ] Correlação com métricas de backend (APM) em ambiente real
