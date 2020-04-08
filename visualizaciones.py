
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para visualizacion de datos
# -- mantiene: Francisco ME
# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME
# -- ------------------------------------------------------------------------------------ -- #



import plotly.graph_objects as go
import plotly.io as pio                           # renderizador para visualizar imagenes
pio.renderers.default = "browser"                 # render de imagenes para correr en script


def plot_ranking(ranking):
    labels = ranking.columns
    values = ranking.values[0]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.2,0.2,0,0,0,0,0,0,0,0,0])])
    fig.show()

def plot_profit_diario(profit_diario):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=profit_diario.index, y=profit_diario.values.T[0], mode = 'lines',
                             name = 'profit diario', line=dict(color='black')))


    fecha_dd = (profit_diario.loc[profit_diario.capital_acm[:profit_diario.capital_acm.idxmin()].idxmax()].name,
                profit_diario.capital_acm.idxmin())
    fecha_du = (profit_diario.loc[profit_diario.capital_acm[:profit_diario.capital_acm.idxmax()].idxmin()].name,
                profit_diario.capital_acm.idxmax())

    fig.add_trace(go.Scatter(x=fecha_dd, y=[profit_diario.capital_acm[:profit_diario.capital_acm.idxmin()].max(),
                                     profit_diario.capital_acm.min()], name = 'drawdown'))

    fig.add_trace(go.Scatter(x=fecha_du, y=[profit_diario.capital_acm[:profit_diario.capital_acm.idxmax()].min(),
                                            profit_diario.capital_acm.max()], name = 'drawup'))

    fig.show()







