# Bug Report - Address Update Endpoint Returned HTTP 503

## Summary

The **Address Update** operation returned **HTTP 503 Service Unavailable** during a controlled performance test execution.

## Severity

High

## Priority

High

## Environment

Homologation-like test environment.

## Tool

Apache JMeter

## Test Configuration

| Item | Value |
|---|---|
| Users | 10 virtual users |
| Ramp-up | 60 seconds |
| Loop count | 1 |
| Test type | Load Test |
| Result format | JTL / Summary Report |

## Steps to Reproduce

1. Configure a JMeter Thread Group with 10 virtual users.
2. Set ramp-up to 60 seconds.
3. Execute the API workflow containing multiple HTTP POST requests.
4. Monitor the response code for the **Address Update** operation.
5. Review the JMeter listener output and generated `.jtl` result file.

## Expected Result

The API operation should return a successful response, such as:

```text
HTTP 200 OK
```

or another valid business response code defined by the API contract.

## Actual Result

The endpoint returned:

```text
HTTP 503 Service Unavailable
```

## Technical Observation

The request reached the server and received a fast HTTP response, which indicates the request was sent successfully by the performance tool. The failure appears to be related to service availability, routing, infrastructure, backend dependency, or endpoint-specific instability.

## Impact

Users may be unable to complete the address update flow when the service is unavailable. This may block a critical business operation and degrade the reliability of the application.

## Evidence

Evidence should include anonymized screenshots or exported reports only:

- Summary Report
- Aggregate Report
- View Results Tree
- JTL result file
- HTML dashboard

## Recommendation

- Validate endpoint health in the target environment.
- Check backend service logs.
- Verify load balancer or gateway routing.
- Confirm whether all required headers, authentication, and session data are present.
- Compare the request with a known working request from an API client.
- Re-execute the test after environment stabilization.

## Confidentiality Note

All names, URLs, identifiers, request bodies, and data used in this report were anonymized for portfolio purposes.
