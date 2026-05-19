import os
import requests
from typing import Any


BASE_URL = "https://apim-proximotrem-prd-brazilsouth-001.azure-api.net/api/v1"


class APIClient:
    def __init__(self, subscription_key: str | None = None, timeout: int = 10):
        key = subscription_key or os.getenv("VIAMOBILIDADE_API_KEY")
        if not key:
            raise RuntimeError(
                "Chave da API não configurada. "
                "Defina a variável de ambiente VIAMOBILIDADE_API_KEY."
            )
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Ocp-Apim-Subscription-Key": key,
                "Accept": "*/*",
                "Accept-Language": "pt-BR,pt;q=0.9",
                "Origin": "https://proximotrem.viamobilidade.com.br",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/148.0.0.0 Safari/537.36"
                ),
            }
        )
        self._timeout = timeout

    def get(self, path: str) -> Any:
        url = f"{BASE_URL}{path}"
        response = self._session.get(url, timeout=self._timeout)
        response.raise_for_status()
        return response.json()
