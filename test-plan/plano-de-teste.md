# Plano de Teste de Performance — Immigration Services REST API

| Campo | Valor |
|---|---|
| Projeto | api-performance-testing-jmeter |
| Ferramenta | Apache JMeter 5.6.3 (modo non-GUI) |
| Tipo de teste | Carga (Load Test) |
| Ambiente | Simulado (mock local replicando a API de homologação, sanitizada) |
| Autora | Roseleyne Duarte |
| Última execução | 07/07/2026 |

## 1. Objetivo

Avaliar o comportamento da API de serviços de imigração sob acesso concorrente, medindo tempo de resposta (média e percentis), throughput e percentual de erro por operação, além de verificar a reprodutibilidade do defeito intermitente HTTP 503 documentado em [`docs/bug-report.md`](../docs/bug-report.md).

## 2. Escopo

### 2.1 Em escopo

Sete operações POST da API, executadas em sequência por cada usuário virtual:

| # | Fluxo | Endpoint |
|---|---|---|
| 1 | Registro | `POST /api/v1/registro` |
| 2 | Alteração de Prazo | `POST /api/v1/alteracao-prazo` |
| 3 | Autorização de Residência | `POST /api/v1/autorizacao-residencia` |
| 4 | Segunda via de CRNM | `POST /api/v1/segunda-via-crnm` |
| 5 | Substituição de CRNM | `POST /api/v1/substituicao-crnm` |
| 6 | Solicitar Alteração de Endereço | `POST /api/v1/alteracao-endereco` |
| 7 | Recadastramento Extemporâneo | `POST /api/v1/recadastramento-extemporaneo` |

### 2.2 Fora de escopo

Endpoints reais de produção, dados pessoais reais, segredos de autenticação (tokens/cookies), documentos em Base64 reais e monitoração de infraestrutura do backend.

## 3. Modelo de carga

| Estágio | Usuários | Ramp-up | Loops | Status |
|---|---:|---:|---:|---|
| Baseline (histórico) | 10 | 60s | 1 | Executado (ambiente de homologação) |
| **Carga leve** | **25** | **10s** | **2** | **Executado — resultados neste repositório** |
| Carga média | 50 | 120s | 1 | Planejado |
| Carga alta | 100 | 120s | 1 | Planejado |
| Stress | 200 | 180s | 1 | Planejado |

O plano `immigration-api-load-test.jmx` é parametrizado por propriedades JMeter, sem necessidade de edição do arquivo:

```bash
jmeter -n -t test-plan/immigration-api-load-test.jmx \
  -Jhost=localhost -Jport=8099 -Jthreads=25 -Jrampup=10 -Jloops=2 \
  -l results/results.jtl -e -o results/dashboard
```

## 4. Estrutura do plano JMeter

- **Thread Group** — usuários/ramp-up/loops parametrizados (`${__P(threads,25)}` etc.), ação em erro: *Continue*.
- **HTTP Request Defaults** — host/porta/protocolo parametrizados; connect timeout 10s; response timeout 30s.
- **HTTP Header Manager** — `Content-Type: application/json`, `Accept: application/json`.
- **7 HTTP Samplers** — POST com payload JSON sanitizado (massa fictícia, `__threadNum` para variação por usuário).
- **Response Assertion por sampler** — código HTTP deve casar com `2\d\d`.
- **Listeners** — Summary Report e Aggregate Report (persistência via `.jtl` CSV).

## 5. Métricas e critérios de aceite (SLA de referência)

| Métrica | Critério | Resultado da execução |
|---|---|---|
| Percentual de erro global | < 1% | 0,57% — atendido |
| Percentual de erro por operação | < 1% | 4,00% no fluxo 06 — **violado** |
| Tempo médio de resposta | < 1.000 ms | 700 ms — atendido |
| 90th percentile (global) | < 2.000 ms | 1.125 ms — atendido |
| Throughput sustentado | ≥ 10 req/s | 17,15 req/s — atendido |

## 6. Ambiente de teste

O alvo é um **mock local** (`mock-api/app.py`, Python 3 stdlib) que replica os contratos sanitizados da API de homologação, com latência gaussiana por endpoint e reprodução controlada do defeito intermitente (HTTP 503 em ~2,5% das chamadas do fluxo 06). Isso permite execução reprodutível do plano sem exposição de dados ou infraestrutura reais.

## 7. Critérios de entrada e saída

**Entrada:** ambiente alvo respondendo em `/health`; massa de dados fictícia validada; plano `.jmx` versionado.

**Saída:** execução concluída sem falha de infraestrutura do gerador de carga; `.jtl` gerado; dashboard HTML publicado; erro analisado por operação; defeitos registrados em bug report.

## 8. Riscos

Instabilidade do ambiente alvo; saturação do gerador de carga mascarando resultados (mitigado: CPU/heap monitorados via `jmeter.log`); ausência de autenticação no mock pode subestimar latência real; resultados de ambiente simulado não substituem medição em homologação/produção.
