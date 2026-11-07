""" Regras de decisão da colônia.
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


def sistemas_a_desligar(sistemas):
    """ PROTÓTIPO: sistemas_a_desligar(sistemas: dict): list[str]
    Aplica a prioridade da colônia: sistemas essenciais (suporte de vida, aquecimento, comunicação) nunca entram na lista.
    Entre os não essenciais que estão ligados, a lista sai do que mais consome para o que menos consome, 
    para economizar o máximo desligando o mínimo de sistemas. """

    candidatos = []
    for nome, dados in sistemas.items():
        if dados["essencial"] == False and dados["ligado"] == True:
            candidatos.append({"nome": nome, "consumo": dados["consumo_kwh"]})

    n = len(candidatos)
    for j in range(n - 1):
        for i in range(n - 1):
            if candidatos[i]["consumo"] < candidatos[i + 1]["consumo"]:
                candidatos[i], candidatos[i + 1] = candidatos[i + 1], candidatos[i]

    nomes = []
    for item in candidatos:
        nomes.append(item["nome"])
    return nomes


def decidir(energia, consumo, sistemas):
    """ PROTÓTIPO: decidir(energia, consumo, sistemas): dict
    Roda as regras em ordem de prioridade (da mais grave para a mais leve) e devolve a ação escolhida e os sistemas que devem ser desligados.
    Quando a energia está normal, nenhum sistema é desligado. """
    
    acao = regra_modo_economia(energia, consumo)
    if acao is None:
        acao = regra_energia_baixa(energia)

    if acao is None:
        return {"acao": "NORMAL: operação dentro dos parâmetros", "desligar": []}
    return {"acao": acao, "desligar": sistemas_a_desligar(sistemas)}
