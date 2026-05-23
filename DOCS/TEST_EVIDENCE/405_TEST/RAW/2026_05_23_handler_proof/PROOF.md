# Proof - Error Handler Behavior

Tanggal: 2026-05-23

Metode uji: direct invocation terhadap handler FastAPI ter-registrasi (tanpa network transport), dengan request ASGI mock.

## Ringkasan hasil

- 405: status=405 | code=METHOD_NOT_ALLOWED | message=Method Not Allowed
- 429: status=429 | code=RATE_LIMITED | message=Too many requests from probe
- 503: status=503 | code=SERVICE_UNAVAILABLE | message=Internal server error
- validation_error: status=422 | code=VALIDATION_ERROR | message=Invalid request payload. Field [body -> text]: Field required
- 500: status=500 | code=INTERNAL_SERVER_ERROR | message=Internal server error

## Artefak
- `*_curl_command.txt`: curl command ekuivalen skenario
- `*_headers.txt`: status + headers response
- `*_body.json`: sample response body
- `curl_result_terminal_capture.txt`: snapshot output gaya terminal
- `summary.json`: ringkasan final
