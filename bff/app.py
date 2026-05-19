import os
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from via_mobilidade import ViaMobilidadeAPI
from bff.stations import STATIONS

app = FastAPI(title="Next Train BFF", version="1.0.0")

# Em produção, defina FRONTEND_URL com o domínio do frontend (ex: https://next-train.vercel.app)
_frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[_frontend_url] if _frontend_url != "*" else ["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

SUPPORTED_LINES = {"L8", "L9"}
api = ViaMobilidadeAPI()


@app.get("/lines")
def get_lines():
    """Status operacional das linhas 8 e 9."""
    all_lines = api.status_linhas()
    return [
        {
            "code": l.code,
            "name": l.line,
            "color_hex": l.color_hex,
            "status_code": l.status_code,
            "status_label": l.status_label,
            "operando": l.operando,
            "description": l.description,
        }
        for l in all_lines
        if l.code in (8, 9)
    ]


@app.get("/lines/{linha}/stations")
def get_stations(linha: str = Path(pattern="^[Ll][89]$")):
    """Lista de estações de uma linha."""
    linha = linha.upper()
    stations = STATIONS.get(linha)
    if stations is None:
        raise HTTPException(status_code=404, detail=f"Linha {linha} não suportada")
    return stations


@app.get("/lines/{linha}/stations/{estacao}/next-train")
def get_next_train(
    linha: str = Path(pattern="^[Ll][89]$"),
    estacao: str = Path(min_length=2, max_length=5),
):
    """Próximos trens para uma estação."""
    linha = linha.upper()
    estacao = estacao.upper()

    if linha not in SUPPORTED_LINES:
        raise HTTPException(status_code=404, detail=f"Linha {linha} não suportada")

    known_codes = {s["code"] for s in STATIONS.get(linha, [])}
    if estacao not in known_codes:
        raise HTTPException(status_code=404, detail=f"Estação {estacao} não encontrada na {linha}")

    try:
        trens = api.proximos_trens(linha, estacao)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao consultar API Via Mobilidade: {e}")

    return [
        {
            "linha": t.linha,
            "estacao_origem": t.estacao_origem,
            "estacao_destino": t.estacao_destino,
            "estacao_origem_trem": t.estacao_origem_trem,
            "proximo_em_segundos": t.proximo_em,
            "proximo_em_minutos": t.proximo_em_minutos,
            "hora_previsto_chegada": t.hora_previsto_chegada,
            "atualizado_em": t.atualizado_em,
            "status": t.status,
        }
        for t in trens
    ]
