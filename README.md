# Next Train BFF

Backend for Frontend das linhas 8 e 9 da Via Mobilidade (CPTM).  
Consome a API interna do [Próximo Trem](https://proximotrem.viamobilidade.com.br), enriquece os dados e os expõe ao frontend via endpoints REST.

---

## Stack

- **Python 3.11**
- **FastAPI** + **Uvicorn**
- **Discloud** (deploy — TYPE=site, porta 8080)

---

## Configuração local

```bash
# 1. Clone e entre na pasta
git clone https://github.com/arthur-fenili/next-train-bff
cd next-train-bff

# 2. Crie o ambiente virtual e instale dependências
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com seus valores

# 4. Suba o servidor
uvicorn bff.app:app --reload
```

### Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `VIAMOBILIDADE_API_KEY` | ✅ | Chave `Ocp-Apim-Subscription-Key` da API Via Mobilidade |
| `FRONTEND_URL` | ❌ | Origem permitida no CORS (ex: `https://next-train.vercel.app`). Use `*` para liberar tudo em desenvolvimento |

---

## Rotas

### `GET /lines`

Retorna o status operacional das linhas 8 e 9.

**Resposta**
```json
[
  {
    "code": 8,
    "name": "Diamante",
    "color_hex": "#949488",
    "status_code": 1,
    "status_label": "Normal",
    "operando": true,
    "description": "Operação normal em toda a linha."
  },
  {
    "code": 9,
    "name": "Esmeralda",
    "color_hex": "#219896",
    "status_code": 1,
    "status_label": "Normal",
    "operando": true,
    "description": "Operação normal em toda a linha."
  }
]
```

---

### `GET /lines/{linha}/stations`

Lista todas as estações de uma linha com seus códigos internos.

**Parâmetros de rota**

| Parâmetro | Formato | Exemplo |
|---|---|---|
| `linha` | `L8` ou `L9` (case-insensitive) | `L8` |

**Resposta**
```json
[
  { "code": "JPR", "name": "Júlio Prestes" },
  { "code": "BFU", "name": "Palmeiras-Barra Funda" }
]
```

---

### `GET /lines/{linha}/stations/{estacao}/next-train`

Retorna os próximos trens previstos para uma estação, enriquecidos com o campo `sentido`.

**Parâmetros de rota**

| Parâmetro | Formato | Exemplo |
|---|---|---|
| `linha` | `L8` ou `L9` (case-insensitive) | `L9` |
| `estacao` | Código de 3 letras | `PIN` |

**Resposta**
```json
[
  {
    "linha": "L9",
    "estacao_origem": "PIN",
    "estacao_destino": "OSA",
    "estacao_origem_trem": "CJD",
    "sentido": "Osasco",
    "proximo_em_segundos": 240,
    "proximo_em_minutos": 4,
    "hora_previsto_chegada": "22:14",
    "atualizado_em": "2026-05-19T22:10:00",
    "status": "deslocamento"
  }
]
```

**Campo `sentido`**  
Determinado pelo BFF comparando os índices de `estacao_origem` e `estacao_destino` na lista ordenada de estações. Retorna sempre o nome do terminal:

| Linha | Terminal inicial | Terminal final |
|---|---|---|
| L8 | Júlio Prestes | Itapevi |
| L9 | Osasco | Varginha |

**Códigos de `status`**

| Valor | Significado |
|---|---|
| `plataforma` | Trem parado na plataforma |
| `deslocamento` | Trem em movimento |

**Erros possíveis**

| Código | Motivo |
|---|---|
| `404` | Linha ou estação não encontrada |
| `502` | Falha na comunicação com a API Via Mobilidade |

---

## Mapeamento de estações e códigos

### Linha 8 — Diamante

| Código | Estação |
|---|---|
| `JPR` | Júlio Prestes |
| `BFU` | Palmeiras-Barra Funda |
| `LAB` | Lapa |
| `DMO` | Domingos de Moraes |
| `ILE` | Imperatriz Leopoldina |
| `PAL` | Presidente Altino |
| `OSA` | Osasco |
| `CSA` | Comandante Sampaio |
| `QTU` | Quitaúna |
| `GMC` | General Miguel Costa |
| `CPB` | Carapicuíba |
| `STE` | Santa Terezinha |
| `AJO` | Antônio João |
| `BRU` | Barueri |
| `JBE` | Jardim Belval |
| `JSI` | Jardim Silveira |
| `JDI` | Jandira |
| `SCO` | Sagrado Coração |
| `ECD` | Engenheiro Cardoso |
| `IPV` | Itapevi |
| `SRT` | Santa Rita |
| `AMB` | Ambuitá |
| `ABU` | Amador Bueno |

### Linha 9 — Esmeralda

| Código | Estação |
|---|---|
| `OSA` | Osasco |
| `PAL` | Presidente Altino |
| `CEA` | Ceasa |
| `JAG` | Vila Lobos-Jaguaré |
| `USP` | Cidade Universitária |
| `PIN` | Pinheiros |
| `HBR` | Hebraica-Rebouças |
| `CJD` | Cidade Jardim |
| `VOL` | Vila Olímpia |
| `BRR` | Berrini |
| `MRB` | Morumbi |
| `GJT` | Granja Julieta |
| `JOD` | João Dias |
| `SAM` | Santo Amaro |
| `SOC` | Socorro |
| `JUR` | Jurubatuba |
| `AUT` | Autódromo |
| `INT` | Primavera-Interlagos |
| `GRA` | Grajaú |
| `MVN` | Bruno Covas/Mendes-Vila Natal |
| `VAG` | Varginha |


---

## Estrutura do projeto

```
next-train-bff/
├── bff/
│   ├── app.py          # FastAPI — rotas e lógica de enriquecimento
│   └── stations.py     # Mapeamento código → nome das estações
├── via_mobilidade/
│   ├── __init__.py
│   ├── api.py          # Métodos de alto nível (status, próximos trens)
│   ├── client.py       # HTTP client com autenticação
│   └── models.py       # Dataclasses de resposta
├── requirements.txt
├── discloud.config
└── .env.example
```
