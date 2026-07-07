# JMeter Immigration API Performance Testing

Sample performance testing project using **Apache JMeter** for a fictitious Immigration Services REST API.

This repository was created as a QA/SDET portfolio project to demonstrate performance testing strategy, load execution, result analysis, and defect documentation.

## Disclaimer

This project is based on a real-world performance testing scenario. All system names, business names, endpoint names, URLs, payloads, identifiers, files, and test data have been anonymized or replaced with fictitious examples to preserve confidentiality.

No production data, real endpoint, token, cookie, Base64 file, personal information, client name, or private system reference is included.

## Objective

Validate the behavior of multiple REST API operations under a controlled load scenario and document one relevant defect observed during execution.

## Tools

- Apache JMeter
- HTTP Request Samplers
- Summary Report
- JTL result file
- CSV-based result analysis
- Markdown documentation

## Test Scenario

| Item | Value |
|---|---|
| Test type | Load Test |
| Users | 10 virtual users |
| Ramp-up | 60 seconds |
| Loop count | 1 |
| Environment | Homologation-like test environment |
| Data | Fictitious/anonymized |

## Sanitized API Operations

| Operation | Description |
|---|---|
| User Registration | Creates a fictitious user registration request |
| Permit Extension | Simulates extension/update of an existing permit |
| Residence Authorization | Simulates authorization request validation |
| Document Reissue | Simulates a second copy/reissue request |
| Document Replacement | Simulates document replacement flow |
| Address Update | Simulates residential address update |
| User Revalidation | Simulates late or additional user revalidation |

## Metrics Observed

- Response time
- Average response time
- Minimum and maximum response time
- Throughput
- Error percentage
- HTTP status codes
- Request/response behavior

## Defect Documented

During investigation, one endpoint returned:

```text
HTTP 503 Service Unavailable
```

The issue was documented as a potential service unavailability or backend dependency instability. See:

```text
docs/bug-report.md
```

## Repository Structure

```text
jmeter-immigration-api-performance
├── README.md
├── .gitignore
├── docs
│   ├── bug-report.md
│   ├── performance-report.md
│   └── test-strategy.md
├── results
│   └── sample-summary-sanitized.csv
├── test-plan
│   └── sanitized-test-plan-notes.md
└── evidence
    └── evidence-placeholder.md
```

## How to Use

1. Open Apache JMeter.
2. Create or import your own `.jmx` test plan.
3. Use the sanitized operation names from this repository.
4. Save execution results as `.jtl`.
5. Generate the HTML dashboard using:

```bash
jmeter -g results/performance_results.jtl -o reports/dashboard
```

## Recommended GitHub Topics

```text
jmeter
performance-testing
load-testing
qa
sdet
api-testing
software-testing
test-automation
```

## Author

QA/SDET portfolio project focused on performance testing, analysis, and defect documentation.
