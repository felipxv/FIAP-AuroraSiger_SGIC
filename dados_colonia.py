# Dados da colônia Aurora Siger.
# Tudo fica em dicionários e listas comuns do Python. A colônia é um dicionário
# hierárquico: cada chave é um sistema e, quando o sistema tem subsistemas, o
# valor é outro dicionário dentro dele (energia -> solar / eólica).
#
#   colonia
#   ├── energia
#   │   ├── solar        (geração em kWh e status)
#   │   ├── eolica       (geração em kWh e status)
#   │   ├── nivel_percentual / consumo_percentual  (usados nas regras de decisão)
#   │   └── consumo_kwh / reserva_kwh              (usados na análise de energia)
#   ├── clima            (temperatura, vento, tempestade)
#   └── sistemas         (suporte de vida, comunicação, laboratório...)
colonia = {
    "energia": {
        "nivel_percentual": 42,
        "consumo_percentual": 68,
        "solar": {"geracao_kwh": 42.0, "status": "operacional"},
        "eolica": {"geracao_kwh": 18.5, "status": "operacional"},
        "consumo_kwh": 70.0,
        "reserva_kwh": 120.0,
    },
    "clima": {
        "temperatura_c": -40.0,
        "vento_kmh": 11.0,
        "tempestade": False,
    },
    "sistemas": {
        "suporte_vida":       {"essencial": True,  "ligado": True, "consumo_kwh": 25.0},
        "aquecimento":        {"essencial": True,  "ligado": True, "consumo_kwh": 30.0},
        "comunicacao":        {"essencial": True,  "ligado": True, "consumo_kwh": 8.0},
        "laboratorio":        {"essencial": False, "ligado": True, "consumo_kwh": 15.0},
        "iluminacao_externa": {"essencial": False, "ligado": True, "consumo_kwh": 12.0},
        "estufa":             {"essencial": False, "ligado": True, "consumo_kwh": 20.0},
    },
}
