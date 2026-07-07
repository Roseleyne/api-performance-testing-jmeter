# Summary Report

Execução: 25 usuários virtuais | ramp-up 10s | 2 loops | ambiente simulado (mock local)

| Label | # Samples | Average | Min | Max | Std. Dev. | Error % | Throughput | Received KB/sec | Sent KB/sec | Avg. Bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 - Registro | 50 | 895 | 264 | 1685 | 256.61 | 0.00% | 3.20/sec | 0.85 | 1.86 | 273 |
| 02 - Alteracao de Prazo | 50 | 556 | 252 | 932 | 172.02 | 0.00% | 3.22/sec | 0.86 | 1.91 | 273 |
| 03 - Autorizacao de Residencia | 50 | 631 | 212 | 1349 | 309.08 | 0.00% | 3.14/sec | 0.84 | 1.91 | 273 |
| 04 - Segunda via de CRNM | 50 | 629 | 192 | 1105 | 225.12 | 0.00% | 3.06/sec | 0.81 | 1.82 | 273 |
| 05 - Substituicao de CRNM | 50 | 651 | 202 | 1163 | 251.55 | 0.00% | 2.97/sec | 0.79 | 1.77 | 273 |
| 06 - Solicitar Alteracao de Endereco | 50 | 686 | 1 | 1465 | 379.60 | 4.00% | 2.91/sec | 0.77 | 1.74 | 271 |
| 07 - Recadastramento Extemporaneo | 50 | 849 | 262 | 1355 | 307.07 | 0.00% | 2.99/sec | 0.80 | 1.85 | 273 |
| TOTAL | 350 | 700 | 1 | 1685 | 301.60 | 0.57% | 17.15/sec | 4.57 | 10.26 | 273 |
