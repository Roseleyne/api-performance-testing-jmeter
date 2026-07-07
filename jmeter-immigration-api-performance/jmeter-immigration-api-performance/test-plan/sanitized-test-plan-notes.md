# Sanitized Test Plan Notes

## Important

The original test plan must not be uploaded publicly if it contains:

- Real URLs
- System names
- Client names
- Tokens
- Cookies
- Personal information
- Base64 document payloads
- Government or private identifiers

## Recommended Sanitized Naming

| Original Meaning | Public Portfolio Name |
|---|---|
| Real system name | Immigration Services API |
| Real endpoint URL | `https://example.test/api/v1/...` |
| Registration operation | User Registration |
| Address change operation | Address Update |
| Reissue operation | Document Reissue |
| Replacement operation | Document Replacement |
| Revalidation operation | User Revalidation |

## Suggested JMeter Configuration

| Field | Value |
|---|---|
| Thread Group users | 10 |
| Ramp-up | 60 |
| Loop count | 1 |
| Listener | Summary Report |
| Result file | `results/performance_results.jtl` |

## Suggested Endpoint Examples

```text
POST /api/v1/user-registration
POST /api/v1/permit-extension
POST /api/v1/residence-authorization
POST /api/v1/document-reissue
POST /api/v1/document-replacement
POST /api/v1/address-update
POST /api/v1/user-revalidation
```

## Payload Guidance

Use fictitious payloads only. Do not upload real request bodies or Base64 files.
