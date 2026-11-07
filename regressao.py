# Regressão linear simples, feita à mão com o método dos mínimos quadrados.
# Uso apenas da biblioteca padrão (sem numpy, pandas ou sklearn).
#
# O modelo é uma reta:  y = b0 + b1 * x
#   b1 = soma((xi - media_x) * (yi - media_y)) / soma((xi - media_x) ** 2)
#   b0 = media_y - b1 * media_x
#
# Aqui x é a velocidade do vento (km/h) e y é a energia eólica gerada (kWh).


def media(valores):
    """ PROTÓTIPO: media(valores: list): float """
    return sum(valores) / len(valores)


def ajustar_reta(x, y):
    """ PROTÓTIPO: ajustar_reta(x: list, y: list): tuple[float, float]
    Encontra a reta que melhor passa pelos pontos (x, y) e devolve o intercepto (b0) e 
    a inclinação (b1). A inclinação diz quanto y aumenta quando x aumenta uma unidade. """
    media_x = media(x)
    media_y = media(y)

    soma_produtos = 0.0
    soma_quadrados = 0.0
    for i in range(len(x)):
        soma_produtos += (x[i] - media_x) * (y[i] - media_y)
        soma_quadrados += (x[i] - media_x) ** 2

    b1 = soma_produtos / soma_quadrados
    b0 = media_y - b1 * media_x
    return b0, b1


def prever(b0, b1, x_novo):
    """ PROTÓTIPO: prever(b0: float, b1: float, x_novo: float): float
    Usa a reta já ajustada para estimar y num valor de x que não está no histórico. """
    return b0 + b1 * x_novo