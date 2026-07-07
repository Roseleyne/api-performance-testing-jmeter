#!/usr/bin/env python3
"""
Mock API - Immigration Services (ambiente simulado)

Servico HTTP local que replica, de forma sanitizada, os 7 fluxos da API de
servicos de imigracao usados no plano de teste JMeter. Nao requer dependencias
externas (somente Python 3 stdlib).

Comportamento simulado:
  - Latencia por endpoint (distribuicao gaussiana truncada), aproximando o
    comportamento observado no ambiente de homologacao original.
  - Instabilidade intermitente no fluxo "Solicitar Alteracao de Endereco",
    retornando HTTP 503 em ~2,5% das chamadas (reproducao controlada do
    defeito documentado em docs/bug-report.md).

Uso:
    python3 app.py [porta]        # porta padrao: 8099
"""

import json
import random
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099

# Modelo de latencia por endpoint: (media_ms, desvio_ms, minimo_ms)
LATENCY_MODEL = {
    "/api/v1/registro":                      (820, 260, 240),
    "/api/v1/alteracao-prazo":               (540, 180, 180),
    "/api/v1/autorizacao-residencia":        (700, 300, 210),
    "/api/v1/segunda-via-crnm":              (610, 220, 190),
    "/api/v1/substituicao-crnm":             (660, 280, 200),
    "/api/v1/alteracao-endereco":            (640, 320, 190),
    "/api/v1/recadastramento-extemporaneo":  (890, 340, 260),
}

# Probabilidade de HTTP 503 no fluxo instavel (defeito conhecido)
FLAKY_ENDPOINT = "/api/v1/alteracao-endereco"
FLAKY_503_RATE = 0.025

PROTOCOL_PREFIX = {
    "/api/v1/registro": "REG",
    "/api/v1/alteracao-prazo": "ALP",
    "/api/v1/autorizacao-residencia": "AUR",
    "/api/v1/segunda-via-crnm": "SVC",
    "/api/v1/substituicao-crnm": "SBC",
    "/api/v1/alteracao-endereco": "ALE",
    "/api/v1/recadastramento-extemporaneo": "REX",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "MockImmigrationAPI/1.0"

    def log_message(self, fmt, *args):  # silencia log por request
        pass

    def _simulate_latency(self, path):
        mean, std, minimum = LATENCY_MODEL[path]
        delay_ms = max(minimum, random.gauss(mean, std))
        time.sleep(delay_ms / 1000.0)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "UP"})
        else:
            self._send_json(404, {"erro": "recurso nao encontrado"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            self.rfile.read(length)  # consome o corpo

        if self.path not in LATENCY_MODEL:
            self._send_json(404, {"erro": "recurso nao encontrado"})
            return

        # Defeito intermitente: 503 rapido (comportamento de proxy/balanceador)
        if self.path == FLAKY_ENDPOINT and random.random() < FLAKY_503_RATE:
            body = b"<html><body><b>Http/1.1 Service Unavailable</b></body></html>"
            self.send_response(503, "Service Unavailable")
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self._simulate_latency(self.path)
        prefix = PROTOCOL_PREFIX[self.path]
        self._send_json(201, {
            "status": "SUCESSO",
            "protocolo": f"{prefix}-{random.randint(100000, 999999)}",
            "mensagem": "Solicitacao registrada com sucesso",
        })


if __name__ == "__main__":
    random.seed()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Mock Immigration API ouvindo em http://localhost:{PORT}")
    server.serve_forever()
