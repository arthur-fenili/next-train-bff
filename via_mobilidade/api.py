from typing import List
from .client import APIClient
from .models import NextTrain, LineStatus


class ViaMobilidadeAPI:
    def __init__(self, subscription_key: str | None = None, timeout: int = 10):
        self._client = APIClient(subscription_key=subscription_key, timeout=timeout)

    def proximos_trens(self, linha: str, estacao: str) -> List[NextTrain]:
        linha = linha.upper()
        estacao = estacao.upper()
        data = self._client.get(f"/lines/{linha}/stations/{estacao}/next-train")
        return [NextTrain.from_dict(item) for item in data]

    def status_linhas(self) -> List[LineStatus]:
        data = self._client.get("/lines")
        return [LineStatus.from_dict(item) for item in data["Data"]]

    def status_linha(self, codigo: int) -> LineStatus | None:
        linhas = self.status_linhas()
        return next((l for l in linhas if l.code == codigo), None)
