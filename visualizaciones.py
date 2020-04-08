
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
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(profit_diario, y="capital_acm", title='DrawDown and DrawUp')
    fig.show()






