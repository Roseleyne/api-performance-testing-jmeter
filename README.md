# JMeter Performance Test - Fluxo SIMIGRA

Este repositório documenta um teste de performance executado com Apache JMeter em um fluxo de serviços HTTP, utilizando dados fictícios e sem exposição de informações sensíveis.

## Objetivo

Validar o comportamento inicial de um conjunto de requisições HTTP em ambiente de homologação, medindo tempo de resposta, throughput e percentual de erro.

## Ferramentas utilizadas

- Apache JMeter 5.6.3
- Summary Report
- View Results Tree para análise pontual
- Arquivo `.jtl` para persistência dos resultados

## Cenário executado

| Configuração | Valor |
|---|---:|
| Usuários virtuais | 10 |
| Ramp-up | 60 segundos |
| Loop Count | 1 |
| Total de amostras | 80 |
| Error % final | 0,00% |

## Fluxos cobertos

- Registro
- Alteração de Prazo
- Autorização de Residência
- Segunda via de CRNM
- Substituição de CRNM
- Solicitar Alteração de Endereço
- Recadastramento Extemporâneo
- Debug Sampler para validação de variáveis

## Resultado resumido

A execução final apresentou sucesso em todos os fluxos, com `0,00%` de erro no Summary Report. Durante a investigação inicial, foi identificado retorno HTTP `503 Service Unavailable` no fluxo **Solicitar Alteração de Endereço**, que posteriormente não se repetiu na execução final.

## Bug localizado

Foi registrado um comportamento instável no endpoint de solicitação de alteração de endereço. Em uma primeira execução, o serviço retornou HTTP `503 Service Unavailable`. Na execução seguinte, com o mesmo plano de teste, o fluxo respondeu com sucesso.

Mais detalhes estão em [`docs/bug-report.md`](docs/bug-report.md).

## Observações de segurança

Este projeto foi sanitizado para publicação no GitHub:

- URLs reais foram mascaradas.
- Dados pessoais foram substituídos por massa fictícia.
- Payloads com documentos/imagens em Base64 foram removidos.
- Tokens, cookies e headers sensíveis não foram incluídos.
- Evidências visuais com dados internos não foram publicadas.

## Como executar localmente

1. Abra o Apache JMeter.
2. Importe ou recrie o plano com base no arquivo de referência em `test-plan/sanitized-test-plan-notes.md`.
3. Configure o caminho do arquivo `.jtl`, por exemplo:

```text
C:\jmeter_results\simigra_resultado_jmeter.jtl
```

4. Execute o teste.
5. Gere o dashboard HTML:

```bash
jmeter -g C:\jmeter_results\simigra_resultado_jmeter.jtl -o C:\jmeter_results\dashboard
```

## Métricas analisadas

- Average response time
- Min / Max response time
- Standard Deviation
- Error percentage
- Throughput
- Sent KB/sec
- Received KB/sec

## Próximos testes sugeridos

| Tipo | Usuários | Ramp-up | Objetivo |
|---|---:|---:|---|
| Carga leve | 25 | 60s | Validar estabilidade inicial |
| Carga média | 50 | 120s | Observar degradação progressiva |
| Carga alta | 100 | 120s | Identificar gargalos |
| Stress | 200 | 180s | Descobrir limite aproximado |
| Spike | 300 | 5s | Simular pico abrupto |
| Soak | 50 | 60s + duração 1h | Validar estabilidade prolongada |
