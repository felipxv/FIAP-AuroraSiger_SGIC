""" A colônia é um dicionário hierárquico, onde cada chave é um sistema, sendo através de subsistemas, 
 o valor é outro dicionário dentro dele (energia -> solar / eólica).

  colonia
  ├── energia
  │   ├── solar        (geração em kWh e status)
  │   ├── eolica       (geração em kWh e status)
  │   ├── nivel_percentual / consumo_percentual  (usados nas regras de decisão)
  │   └── consumo_kwh / reserva_kwh              (usados na análise de energia)
  ├── clima            (temperatura, vento, tempestade)
  └── sistemas         (suporte de vida, comunicação, laboratório...) """

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


def buscar_subsistema(no, caminho):
    """ PROTÓTIPO: buscar_subsistema(no: dict, caminho: list): dict | valor | None
    Navega pela hierarquia seguindo uma lista de chaves, uma por nível (ex.: ["energia", "solar"]).
    É recursiva: a cada chamada tira a primeira chave do caminho e desce um nível, até o caminho acabar.
    Devolve None se alguma chave não existir. """

    if len(caminho) == 0:
        return no
    chave = caminho[0]
    if not isinstance(no, dict) or chave not in no:
        return None
    return buscar_subsistema(no[chave], caminho[1:])


def listar_subsistemas(no, prefixo=""):
    """ PROTÓTIPO: listar_subsistemas(no: dict, prefixo: str): None
    Imprime a árvore da colônia, com um recuo a mais a cada nível.
    Quando o valor é outro dicionário, a função chama a si mesma para aquele nível. """
    
    for chave, valor in no.items():
        if isinstance(valor, dict):
            print(f"{prefixo}{chave}/")
            listar_subsistemas(valor, prefixo + "   ")
        else:
            print(f"{prefixo}{chave}: {valor}")
