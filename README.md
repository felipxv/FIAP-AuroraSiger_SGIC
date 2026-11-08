# SGIC: Sistema de Gestão Inteligente da Colônia

Protótipo em Python da Fase 3 da missão Aurora Siger (FIAP, Ciência da Computação). O sistema representa o funcionamento de uma colônia: organiza os dados em uma hierarquia, toma decisões por regras, prevê a geração de energia eólica com regressão linear simples e compara geração com consumo.

O projeto usa só a biblioteca padrão do Python (sem numpy, pandas ou sklearn). Os dados da colônia e o histórico da turbina são fictícios, criados para a demonstração.

## Estrutura do projeto

O código separa dados, lógica e decisões em arquivos diferentes:

| Arquivo | Papel | Conteúdo |
|---|---|---|
| `dados_colonia.py` | Dados | Dicionário `colonia`, históricos de vento e energia eólica, `buscar_subsistema` e `listar_subsistemas` |
| `regras_decisao.py` | Decisões | `regra_energia_baixa`, `regra_modo_economia`, `sistemas_a_desligar`, `decidir` |
| `regressao.py` | Lógica (previsão) | `media`, `ajustar_reta`, `prever`, `r_quadrado` |
| `analise_energia.py` | Lógica (energia) | `geracao_total`, `analisar_balanco`, `autonomia_horas` |
| `main.py` | Apresentação | Chama as funções acima e mostra os resultados na tela |

## Como funciona

### 1. Organização dos dados

A colônia é um dicionário em que cada chave é um sistema e o valor é outro dicionário com os subsistemas:

```
colonia
├── energia
│   ├── solar        (geração em kWh e status)
│   ├── eolica       (geração em kWh e status)
│   ├── nivel_percentual / consumo_percentual  (usados nas regras)
│   └── consumo_kwh / reserva_kwh              (usados na análise de energia)
├── clima            (temperatura, vento, tempestade)
└── sistemas         (suporte de vida, aquecimento, comunicação, laboratório, iluminação externa, estufa)
```

O consumo de cada sistema soma 70 kWh (18 + 22 + 5 + 9 + 6 + 10), o mesmo valor de `consumo_kwh` da energia.

Duas funções recursivas navegam pela árvore:

- `buscar_subsistema(colonia, ["energia", "solar"])` desce um nível por chave da lista e devolve o que encontrar no fim do caminho, ou `None` se alguma chave não existir.
- `listar_subsistemas(colonia)` imprime a árvore inteira, com um recuo a mais a cada nível.

O histórico da turbina fica em duas listas, em que a posição `i` de cada uma é a mesma medição:

```python
historico_vento  = [6, 8, 9, 10, 12, 14, 15, 18]                        # km/h
historico_eolica = [11.5, 15.0, 17.0, 19.5, 23.0, 26.5, 28.0, 33.0]     # kWh
```

### 2. Regras de decisão

As regras usam valores percentuais (nível de energia e consumo, de 0 a 100):

| Regra | Condição | Saída |
|---|---|---|
| Simples | energia < 50 | `ALERTA: reduzir consumo` |
| Combinada | energia < 50 **e** consumo > 60 | `ALERTA: ativar modo economia` |
| Nenhuma se aplica | — | `NORMAL: operação dentro dos parâmetros` |

`decidir` testa primeiro a regra combinada, que é a mais grave, e só depois a simples. Por isso, com energia 40 e consumo 70, as duas regras são verdadeiras, mas a decisão final é `ALERTA: ativar modo economia`.

Quando há alerta, `sistemas_a_desligar` aplica a prioridade da colônia: sistemas essenciais (suporte de vida, aquecimento e comunicação) nunca são desligados. Os não essenciais que estão ligados são ordenados por bubble sort, do que mais consome para o que menos consome, para economizar o máximo desligando o mínimo de sistemas.

### 3. Previsão com regressão linear simples

`regressao.py` ajusta uma reta `energia = b0 + b1 * vento` pelo método dos mínimos quadrados, calculado à mão:

```
b1 = soma((xi - media_x) * (yi - media_y)) / soma((xi - media_x) ** 2)
b0 = media_y - b1 * media_x
```

- `prever(b0, b1, x)` usa a reta para estimar a energia em uma velocidade de vento nova.
- `r_quadrado` mede o quanto a reta explica os dados (1 é ajuste perfeito).

Resultados:

- Exemplo da atividade (vento `[8, 10, 12]`, energia `[20, 25, 30]`): reta `energia = 0 + 2,5 * vento`; para vento 11, a previsão é **27,5**.
- Histórico da turbina: `energia = 0,87 + 1,81 * vento`, com **R² = 0,997**.

A potência real de uma turbina cresce com o cubo da velocidade do vento. Na faixa de vento do histórico, a reta é uma boa aproximação, mas não deve ser usada muito fora dela.

### 4. Análise de energia

Aqui os valores são em kWh. `geracao_total` soma a geração solar e a eólica, e `analisar_balanco` compara com o consumo:

| Situação | Saída |
|---|---|
| consumo > geração | `ALERTA: consumo maior que geração` |
| geração > consumo | `SUGESTÃO: armazenar energia excedente` |
| iguais | `NORMAL: geração e consumo equilibrados` |

Quando o consumo passa da geração, a diferença sai da reserva. `autonomia_horas` calcula por quantas horas a reserva aguenta esse déficit (`reserva / (consumo - geração)`) e devolve `None` quando não há déficit, porque a reserva não está sendo gasta.

O `main.py` faz a análise duas vezes: com a geração registrada agora e com a geração eólica trocada pela previsão da parte 3, para o vento atual. Com os dados de exemplo, a reta prevê 20,8 kWh para vento de 11 km/h, enquanto a geração eólica registrada é 18,5 kWh. Os dados são fictícios e a reta é uma aproximação, então os dois valores não precisam coincidir.

## Como executar

Requisito: Python 3.12 ou mais recente. Não há dependências para instalar.

```bash
git clone https://github.com/felipxv/FIAP-AuroraSiger_SGIC.git
cd FIAP-AuroraSiger_SGIC
python main.py
```

## Exemplo de entrada e saída

**Entrada** (valores atuais em `dados_colonia.py`): energia 42%, consumo 68%, geração solar 42,0 kWh, geração eólica 18,5 kWh, consumo 70,0 kWh, reserva 120,0 kWh, vento 11 km/h.

**Saída** de `python main.py` (a árvore completa da seção 1 foi encurtada aqui):

```
SGIC: Sistema de Gestão Inteligente da Colônia Aurora Siger

============================================================
1. ESTRUTURA DA COLÔNIA
============================================================
energia/
   nivel_percentual: 42
   consumo_percentual: 68
   solar/
      geracao_kwh: 42.0
      status: operacional
   ...

Navegação: energia -> solar
{'geracao_kwh': 42.0, 'status': 'operacional'}
Navegação: sistemas -> suporte_vida -> consumo_kwh
18.0
Navegação: energia -> nuclear (não existe)
None

============================================================
2. REGRAS DE DECISÃO
============================================================
Estado atual: energia = 42% | consumo = 68%
Regra simples (energia < 50): ALERTA: reduzir consumo
Regra combinada (energia < 50 E consumo > 60): ALERTA: ativar modo economia
Decisão final: ALERTA: ativar modo economia
Sistemas a desligar (do maior para o menor consumo):
   - estufa
   - laboratorio
   - iluminacao_externa
Sistemas essenciais mantidos ligados:
   - suporte_vida
   - aquecimento
   - comunicacao

Cenários de teste (energia %, consumo %):
   (40, 70) -> ALERTA: ativar modo economia
   (40, 50) -> ALERTA: reduzir consumo
   (80, 70) -> NORMAL: operação dentro dos parâmetros

============================================================
3. PREVISÃO (REGRESSÃO LINEAR SIMPLES)
============================================================
Exemplo da atividade: vento = [8, 10, 12] | energia = [20, 25, 30]
   Reta: energia = 0.00 + 2.50 * vento
   Vento 11 -> previsão de 27.5

Histórico da turbina (8 medições):
   Reta: energia = 0.87 + 1.81 * vento
   R² = 0.997
   Vento atual 11.0 km/h -> previsão de 20.8 kWh
   Obs.: a potência real cresce com o cubo do vento; a reta é uma aproximação.

============================================================
4. ANÁLISE DE ENERGIA (kWh)
============================================================
Cenários de teste:
   geração 40 | consumo 70 -> ALERTA: consumo maior que geração
   geração 80 | consumo 30 -> SUGESTÃO: armazenar energia excedente

Colônia agora: solar 42.0 + eólica 18.5 = 60.5 kWh
Consumo: 70.0 kWh | reserva: 120.0 kWh
ALERTA: consumo maior que geração
Autonomia da reserva neste ritmo: 12.6 horas

Com a eólica prevista (20.8 kWh), a geração vai a 62.8 kWh
ALERTA: consumo maior que geração
Autonomia da reserva neste ritmo: 16.6 horas
```

## Como testar

Rodar `python main.py` já exercita todas as funções. Para testar uma função isolada, execute os comandos abaixo na pasta do projeto e compare com o resultado esperado:

```bash
# Regressão: exemplo da atividade (esperado: 27.5)
python -c "from regressao import ajustar_reta, prever; b0, b1 = ajustar_reta([8, 10, 12], [20, 25, 30]); print(prever(b0, b1, 11))"

# Regra combinada vence a simples (esperado: modo economia e estufa, laboratorio, iluminacao_externa)
python -c "from regras_decisao import decidir; from dados_colonia import colonia; print(decidir(40, 70, colonia['sistemas']))"

# Energia normal não desliga nada (esperado: NORMAL e lista vazia)
python -c "from regras_decisao import decidir; from dados_colonia import colonia; print(decidir(80, 70, colonia['sistemas']))"

# Navegação em três níveis (esperado: 18.5)
python -c "from dados_colonia import colonia, buscar_subsistema; print(buscar_subsistema(colonia, ['energia', 'eolica', 'geracao_kwh']))"

# Balanço equilibrado (esperado: NORMAL: geração e consumo equilibrados)
python -c "from analise_energia import analisar_balanco; print(analisar_balanco(50, 50))"

# Autonomia com déficit de 9,5 kWh (esperado: 12.6)
python -c "from analise_energia import autonomia_horas; print(round(autonomia_horas(120, 60.5, 70), 1))"

# Sem déficit a reserva não é usada (esperado: None)
python -c "from analise_energia import autonomia_horas; print(autonomia_horas(120, 80, 70))"
```

Para simular outra situação, altere os valores em `dados_colonia.py` e rode `python main.py` de novo. Por exemplo, com `nivel_percentual` em 80 a decisão passa a ser NORMAL; com `consumo_kwh` em 50.0 a análise sugere armazenar o excedente e informa que a reserva não está sendo usada.

## Como o sistema ajuda no uso de energia

- Detecta energia baixa e consumo alto e indica a ação certa para cada caso.
- Escolhe quais sistemas desligar sem tocar nos essenciais, começando pelos que mais consomem.
- Prevê quanto a turbina vai gerar com o vento esperado, o que permite planejar o consumo antes de faltar energia.
- Avisa quando o consumo passa da geração e sugere armazenar o excedente quando sobra energia.
- Calcula por quantas horas a reserva aguenta o déficit, agora e com a geração prevista, para mostrar quanto tempo a colônia tem para reagir.
