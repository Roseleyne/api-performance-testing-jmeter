# Performance Test Strategy

## Scope

This sample project demonstrates a controlled load test against a fictitious Immigration Services REST API.

## Goals

- Validate API behavior under concurrent access.
- Identify unstable endpoints.
- Capture response times and error rates.
- Document defects using professional QA standards.
- Produce reusable evidence for a QA/SDET portfolio.

## Out of Scope

- Real production endpoints.
- Real personal data.
- Real government or client identifiers.
- Authentication secrets, cookies, tokens, or Base64 documents.
- Infrastructure-level monitoring.

## Load Model

| Stage | Users | Ramp-up | Loop |
|---|---:|---:|---:|
| Baseline | 10 | 60 seconds | 1 |
| Light Load | 25 | 60 seconds | 1 |
| Medium Load | 50 | 120 seconds | 1 |
| High Load | 100 | 120 seconds | 1 |
| Stress | 200 | 180 seconds | 1 |

## Entry Criteria

- Test environment available.
- Test data prepared and anonymized.
- API endpoints reachable.
- No real credentials stored in the repository.

## Exit Criteria

- Execution completed.
- JTL result generated.
- Error percentage analyzed.
- Critical issues documented.
- Evidence stored using sanitized screenshots or reports.

## Risks

- Environment instability.
- Backend service unavailability.
- Missing authentication/session dependencies.
- Incomplete observability data.
- Rate limiting or gateway restrictions.
