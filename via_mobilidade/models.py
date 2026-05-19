from dataclasses import dataclass
from typing import Optional


@dataclass
class NextTrain:
    linha: str
    estacao_origem: str
    estacao_destino: str
    estacao_origem_trem: str
    proximo_em: int  # segundos
    hora_previsto_chegada: str
    atualizado_em: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "NextTrain":
        return cls(
            linha=data["linha"],
            estacao_origem=data["estacao_origem"],
            estacao_destino=data["estacao_destino"],
            estacao_origem_trem=data["estacao_origem_trem"],
            proximo_em=data["proximo_em"],
            hora_previsto_chegada=data["hora_previsto_chegada"],
            atualizado_em=data["atualizado_em"],
            status=data["status"],
        )

    @property
    def proximo_em_minutos(self) -> float:
        return round(self.proximo_em / 60, 1)


@dataclass
class LineStatus:
    code: int
    color_name: str
    color_hex: str
    line: str
    status_code: str
    status_label: str
    status_color: str
    description: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "LineStatus":
        return cls(
            code=data["Code"],
            color_name=data["ColorName"],
            color_hex=data["ColorHex"],
            line=data["Line"],
            status_code=data["StatusCode"],
            status_label=data["StatusLabel"],
            status_color=data["StatusColor"],
            description=data.get("Description"),
        )

    @property
    def operando(self) -> bool:
        return self.status_code == "OperacaoNormal"
