# Relatório Executivo — Teste de Performance da API de Serviços de Imigração

**Data da execução:** 07/07/2026 · **Ferramenta:** Apache JMeter 5.6.3 · **Cenário:** carga leve (25 usuários simultâneos, 350 requisições) · **Ambiente:** simulado (mock sanitizado)

## Resumo

O teste de carga avaliou as 7 operações críticas da API (registro, alterações cadastrais, emissão e substituição de documentos). O sistema **atendeu aos critérios globais de desempenho**: tempo médio de resposta de **700 ms**, 90% das requisições respondidas em até **1,13 s** e vazão sustentada de **17 requisições/segundo**, acima da meta de 10 req/s.

## Principal ponto de atenção

A operação **Solicitar Alteração de Endereço** apresentou **4% de falhas** (HTTP 503 – Serviço Indisponível), violando o critério de no máximo 1% de erro por operação. Este é o mesmo defeito intermitente identificado na rodada baseline anterior — agora **reproduzido sob carga**, o que confirma que não se tratou de evento isolado. Detalhes em [`bug-report.md`](bug-report.md).

## Resultado por critério

| Critério | Meta | Resultado | Situação |
|---|---|---|---|
| Erro global | < 1% | 0,57% | ✅ Atendido |
| Erro por operação | < 1% | 4,00% (Alteração de Endereço) | ❌ Violado |
| Tempo médio | < 1s | 0,70s | ✅ Atendido |
| 90% das respostas | < 2s | 1,13s | ✅ Atendido |
| Vazão | ≥ 10 req/s | 17,15 req/s | ✅ Atendido |

## Recomendações

1. **Priorizar a correção da instabilidade** no serviço de alteração de endereço antes da próxima janela de release — o comportamento indica falha no balanceador/proxy ou saturação pontual do serviço.
2. Executar as rodadas de **carga média (50 VUs) e alta (100 VUs)** após a correção, para validar a estabilidade sob volumes maiores.
3. Incluir a operação afetada em **monitoração contínua** (alertas para respostas 5xx).

## Veredicto

**Aprovado com ressalva.** O desempenho geral é adequado para o volume testado, porém a instabilidade recorrente no fluxo de alteração de endereço deve ser tratada como impeditivo para aumento de carga em produção.
