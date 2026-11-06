"""  Regras de decisão da colônia.
 Cada regra é uma condição simples ou combinada (and / or) que devolve uma ação clara quando é verdadeira, ou None quando não se aplica. """

LIMITE_ENERGIA = 50    # abaixo disso, energia considerada baixa
LIMITE_CONSUMO = 60    # acima disso, consumo considerado alto


def regra_energia_baixa(energia, limite=LIMITE_ENERGIA):
    """ PROTÓTIPO: regra_energia_baixa(energia: float, limite: float): str | None
    Regra simples: SE energia < limite ENTÃO reduzir consumo. """
    if energia < limite:
        return "ALERTA: reduzir consumo"
    return None


def regra_modo_economia(energia, consumo, limite_energia=LIMITE_ENERGIA, limite_consumo=LIMITE_CONSUMO):
    """ PROTÓTIPO: regra_modo_economia(energia, consumo, limite_energia, limite_consumo): str | None
    Regra combinada: SE energia < limite_energia E consumo > limite_consumo ENTÃO ativar modo economia.
    As duas condições precisam ser verdadeiras ao mesmo tempo, por isso é mais grave que a regra simples. """
    if energia < limite_energia and consumo > limite_consumo:
        return "ALERTA: ativar modo economia"
    return None
