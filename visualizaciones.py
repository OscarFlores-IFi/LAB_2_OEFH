
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para visualizacion de datos
# -- mantiene: Francisco ME
# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME
# -- ------------------------------------------------------------------------------------ -- #



import plotly.graph_objects as go
import plotly.io as pio                           # renderizador para visualizar imagenes
pio.renderers.default = "browser"                 # render de imagenes para correr en script
import plotly.express as px


def plot_ranking(ranking):
    labels = ranking.columns
    values = ranking.values[0]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1,0.1,0,0,0,0,0,0,0,0,0])])
    fig.update_layout(
        title="Rankings",
        )
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
    fig.update_layout(
        title="Profit & DrawUp/Down",
        xaxis_title="Time",
        yaxis_title="Portfolio value",
        )
    fig.show()

def plot_sesgos(sesgos2):
    fig = px.bar(sesgos2, x=sesgos2.index, y='valores')
    fig.update_layout(
        title="Sesgos",
        xaxis_title="Variables",
        yaxis_title="cantidad/porcentage",
        )
    fig.show()



