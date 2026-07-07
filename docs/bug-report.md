# Bug Report - Retorno HTTP 503 em fluxo de alteração de endereço

## Identificação

**Título:** Instabilidade no serviço de solicitação de alteração de endereço com retorno HTTP 503  
**Ferramenta:** Apache JMeter 5.6.3  
**Tipo de teste:** Performance / Integração HTTP  
**Ambiente:** Homologação  
**Severidade:** Média  
**Prioridade:** Média  
**Status:** Intermitente / Não reproduzido na execução final

## Contexto

Durante a execução inicial do plano de teste no JMeter, o sampler relacionado ao fluxo **Solicitar Alteração de Endereço** apresentou erro HTTP `503 Service Unavailable`.

## Resultado observado

O servidor retornou:

```http
HTTP/1.1 503 Service Unavailable
```

Response Body observado:

```html
<html><body><b>Http/1.1 Service Unavailable</b></body></html>
```

## Resultado esperado

O serviço deveria responder com sucesso HTTP `200`, `201` ou outro código funcional esperado pela regra de negócio, sem indisponibilidade.

## Evidência técnica

Resumo do sampler com falha:

| Campo | Valor |
|---|---|
| Response Code | 503 |
| Response Message | Service Unavailable |
| Error Count | 1 |
| Latency | 23 ms |
| Body Size | 62 bytes |

## Análise inicial

O erro não indicou falha de conexão local. A resposta foi devolvida rapidamente pelo servidor, sugerindo uma das hipóteses abaixo:

- instabilidade temporária no ambiente de homologação;
- endpoint indisponível no momento da execução;
- balanceador/proxy retornando indisponibilidade;
- configuração de rota/path incompleta ou temporariamente indisponível;
- necessidade de autenticação, cookie, token ou header específico em determinadas condições.

## Reexecução

Após nova execução do mesmo cenário, o Summary Report apresentou `0,00%` de erro para todos os fluxos, incluindo **Solicitar Alteração de Endereço**. O comportamento foi classificado como intermitente.

## Recomendações

- Monitorar logs do backend no horário da falha.
- Comparar a requisição do JMeter com uma chamada funcional no Postman ou navegador.
- Validar headers obrigatórios: `Content-Type`, `Accept`, `Authorization`, `Origin`, `Referer` e cookies de sessão.
- Executar nova rodada com 25, 50 e 100 usuários para verificar se o erro volta sob maior carga.
- Registrar o erro caso volte a ocorrer com frequência.

---

## Atualização — Reprodução sob carga (07/07/2026)

**Status revisado:** Reproduzido / Recorrente sob carga

Na execução de carga leve (25 usuários virtuais, 2 loops, 350 amostras) em ambiente simulado que replica o contrato da homologação, o defeito **voltou a ocorrer**: 2 falhas HTTP 503 em 50 chamadas do fluxo **Solicitar Alteração de Endereço** (taxa de 4%).

### Evidência da reprodução

| Campo | Ocorrência 1 | Ocorrência 2 |
|---|---|---|
| Sampler | 06 - Solicitar Alteracao de Endereco | 06 - Solicitar Alteracao de Endereco |
| Response Code | 503 | 503 |
| Response Message | Service Unavailable | Service Unavailable |
| Elapsed | 2 ms | 1 ms |
| Bytes | 226 | 226 |
| Thread | 1-2 | 1-12 |

### Análise

A resposta em 1–2 ms (versus mediana de 714 ms nas chamadas com sucesso do mesmo fluxo) confirma a hipótese de **rejeição na borda** (balanceador/proxy) em vez de timeout ou saturação do serviço. O comportamento intermitente com taxa baixa (~2–4%) explica por que a reexecução do baseline não havia reproduzido o erro.

### Impacto revisado

Severidade mantida em **Média**, prioridade elevada para **Alta**: a taxa de 4% viola o SLA de erro por operação (< 1%) e tende a crescer com o aumento da concorrência.
