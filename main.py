""" SGIC: Sistema de Gestão Inteligente da Colônia (missão Aurora Siger).
 Este arquivo só apresenta os resultados: os dados ficam em dados_colonia.py, os cálculos em regressao.py e
 analise_energia.py, e as decisões em regras_decisao.py. """

from dados_colonia import colonia, historico_vento, historico_eolica, buscar_subsistema, listar_subsistemas
from regras_decisao import regra_energia_baixa, regra_modo_economia, decidir
from regressao import ajustar_reta, prever, r_quadrado
from analise_energia import geracao_total, analisar_balanco, autonomia_horas


def titulo(texto):
    """ PROTÓTIPO: titulo(texto: str): None
    Imprime o nome de cada parte do relatório entre linhas, para separar as seções na tela. """

    print()
    print("=" * 60)
    print(texto)
    print("=" * 60)


def mostrar_estrutura():
    """ PROTÓTIPO: mostrar_estrutura(): None
    Mostra a árvore da colônia e um exemplo de navegação entre subsistemas. """

    titulo("1. ESTRUTURA DA COLÔNIA")
    listar_subsistemas(colonia)

    print()
    print("Navegação: energia -> solar")
    print(buscar_subsistema(colonia, ["energia", "solar"]))
    print("Navegação: sistemas -> suporte_vida -> consumo_kwh")
    print(buscar_subsistema(colonia, ["sistemas", "suporte_vida", "consumo_kwh"]))
    print("Navegação: energia -> nuclear (não existe)")
    print(buscar_subsistema(colonia, ["energia", "nuclear"]))


def mostrar_regras():
    """ PROTÓTIPO: mostrar_regras(): None
    Aplica as regras ao estado atual da colônia e a alguns cenários de teste. """

    titulo("2. REGRAS DE DECISÃO")
    energia = colonia["energia"]["nivel_percentual"]
    consumo = colonia["energia"]["consumo_percentual"]

    print(f"Estado atual: energia = {energia}% | consumo = {consumo}%")
    print(f"Regra simples (energia < 50): {regra_energia_baixa(energia)}")
    print(f"Regra combinada (energia < 50 E consumo > 60): {regra_modo_economia(energia, consumo)}")

    decisao = decidir(energia, consumo, colonia["sistemas"])
    print(f"Decisão final: {decisao['acao']}")
    print("Sistemas a desligar (do maior para o menor consumo):")
    for nome in decisao["desligar"]:
        print(f"   - {nome}")
    print("Sistemas essenciais mantidos ligados:")
    for nome, dados in colonia["sistemas"].items():
        if dados["essencial"]:
            print(f"   - {nome}")

    print()
    print("Cenários de teste (energia %, consumo %):")
    cenarios = [(40, 70), (40, 50), (80, 70)]
    for energia_teste, consumo_teste in cenarios:
        resultado = decidir(energia_teste, consumo_teste, colonia["sistemas"])
        print(f"   ({energia_teste}, {consumo_teste}) -> {resultado['acao']}")


def mostrar_previsao():
    """ PROTÓTIPO: mostrar_previsao(): float
    Ajusta a reta no exemplo da atividade e no histórico da turbina e faz as previsões.
    Devolve a energia eólica prevista, que a parte 4 usa. """

    titulo("3. PREVISÃO (REGRESSÃO LINEAR SIMPLES)")

    vento = [8, 10, 12]
    energia = [20, 25, 30]
    b0, b1 = ajustar_reta(vento, energia)
    print(f"Exemplo da atividade: vento = {vento} | energia = {energia}")
    print(f"   Reta: energia = {b0:.2f} + {b1:.2f} * vento")
    print(f"   Vento 11 -> previsão de {prever(b0, b1, 11):.1f}")

    print()
    b0, b1 = ajustar_reta(historico_vento, historico_eolica)
    r2 = r_quadrado(historico_vento, historico_eolica, b0, b1)
    vento_atual = colonia["clima"]["vento_kmh"]
    print(f"Histórico da turbina ({len(historico_vento)} medições):")
    print(f"   Reta: energia = {b0:.2f} + {b1:.2f} * vento")
    print(f"   R² = {r2:.3f}")
    previsao = prever(b0, b1, vento_atual)
    print(f"   Vento atual {vento_atual} km/h -> previsão de {previsao:.1f} kWh")
    print("   Obs.: a potência real cresce com o cubo do vento; a reta é uma aproximação.")
    return previsao


def mostrar_autonomia(reserva, geracao, consumo):
    """ PROTÓTIPO: mostrar_autonomia(reserva: float, geracao: float, consumo: float): None
    Mostra por quantas horas a reserva aguenta, ou avisa que não há déficit. """

    horas = autonomia_horas(reserva, geracao, consumo)
    if horas is None:
        print("Autonomia da reserva: sem déficit, a reserva não está sendo usada.")
    else:
        print(f"Autonomia da reserva neste ritmo: {horas:.1f} horas")


def mostrar_analise_energia(previsao):
    """ PROTÓTIPO: mostrar_analise_energia(previsao: float): None
    Compara a geração com o consumo da colônia, agora e com a geração eólica prevista. """

    titulo("4. ANÁLISE DE ENERGIA (kWh)")
    print("Exemplos da atividade:")
    for geracao_teste, consumo_teste in [(40, 70), (80, 30)]:
        print(f"   geração {geracao_teste} | consumo {consumo_teste} -> {analisar_balanco(geracao_teste, consumo_teste)}")

    energia = colonia["energia"]
    geracao = geracao_total(energia)
    consumo = energia["consumo_kwh"]
    reserva = energia["reserva_kwh"]

    print()
    print(f"Colônia agora: solar {energia['solar']['geracao_kwh']} + eólica {energia['eolica']['geracao_kwh']} = {geracao} kWh")
    print(f"Consumo: {consumo} kWh | reserva: {reserva} kWh")
    print(analisar_balanco(geracao, consumo))
    mostrar_autonomia(reserva, geracao, consumo)

    # A turbina passa a valer a previsão feita na parte 3
    geracao_prevista = energia["solar"]["geracao_kwh"] + previsao
    print()
    print(f"Com a eólica prevista ({previsao:.1f} kWh), a geração vai a {geracao_prevista:.1f} kWh")
    print(analisar_balanco(geracao_prevista, consumo))
    mostrar_autonomia(reserva, geracao_prevista, consumo)


def main():
    """ PROTÓTIPO: main(): None
    Roda as quatro partes do sistema em sequência. """

    print("SGIC: Sistema de Gestão Inteligente da Colônia Aurora Siger")
    mostrar_estrutura()
    mostrar_regras()
    previsao = mostrar_previsao()
    mostrar_analise_energia(previsao)


if __name__ == "__main__":
    main()
