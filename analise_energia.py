# Análise do uso de energia: compara geração, consumo e reserva e transforma
# a comparação numa ação simples.


def geracao_total(energia):
    """PROTÓTIPO: geracao_total(energia: dict): float
    Soma a geração dos dois subsistemas de energia (solar e eólico).
    """
    return energia["solar"]["geracao_kwh"] + energia["eolica"]["geracao_kwh"]


def analisar_balanco(geracao, consumo):
    """PROTÓTIPO: analisar_balanco(geracao: float, consumo: float): str
    Se o consumo passa da geração há risco de faltar energia; se a geração
    passa do consumo, a sobra pode ser guardada em vez de desperdiçada.
    """
    if consumo > geracao:
        return "ALERTA: consumo maior que geração"
    elif geracao > consumo:
        return "SUGESTÃO: armazenar energia excedente"
    else:
        return "NORMAL: geração e consumo equilibrados"
