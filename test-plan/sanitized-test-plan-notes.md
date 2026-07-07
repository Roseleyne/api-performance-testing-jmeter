# Plano de Teste Sanitizado - JMeter

Este arquivo descreve a estrutura do plano executado, sem expor URL real, payload real, tokens, cookies ou dados sensíveis.

## Thread Group

| Campo | Valor |
|---|---:|
| Number of Threads | 10 |
| Ramp-up period | 60 segundos |
| Loop Count | 1 |
| Action after sampler error | Continue |

## Samplers HTTP

A estrutura do plano contém os seguintes samplers:

1. Registro
2. Alteração de Prazo
3. Autorização de Residência
4. Segunda via de CRNM
5. Substituição de CRNM
6. Solicitar Alteração de Endereço
7. Recadastramento Extemporâneo
8. Debug Sampler

## Exemplo de endpoint sanitizado

```text
POST https://<host-homologacao-mascarado>/<path-api-mascarado>
```

## Exemplo de payload sanitizado

```json
{
  "dadosPessoais": {
    "nome": "USUARIO_TESTE",
    "sobrenome": "AUTOMACAO",
    "email": "teste@example.com",
    "documentoIdentidade": {
      "conteudo": "<base64-removido>",
      "extensao": "jpg",
      "mimeType": "image/jpeg"
    }
  },
  "dadosEndereco": {
    "telefoneContato": "00000000000",
    "enderecoResidencial": {
      "logradouro": "RUA TESTE",
      "bairro": "CENTRO",
      "cep": "00000-000",
      "comprovanteEndereco": {
        "conteudo": "<base64-removido>",
        "extensao": "jpg",
        "mimeType": "image/jpeg"
      }
    }
  }
}
```

## Listeners usados

- Summary Report
- Aggregate Report
- View Results Tree somente para debug local

## Observação

Para publicação no GitHub, não versionar arquivos `.jtl` reais com payload, tokens ou dados internos. Utilizar apenas resultados agregados ou arquivos sanitizados.
