
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Oscar Flores
# -- repositorio: https://github.com/OscarFlores-IFi/LAB_2_OEFH
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np




# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_leer_archivo(param_archivo):
    """
    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer

    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido

    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.csv'

    """

    df_data = pd.read_csv('archivos/' + param_archivo)
    df_data.columns = [i.lower() for i in list(df_data.columns)]
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)
    return df_data




# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento

def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : nombre de instrumento

    Returns
    -------
    pips_inst : func : valor en pips del instrumento seleccionado

    Debugging
    -------
    param_ins = 'usdjpy'
    """

    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pips_inst[inst]




# -- ------------------------------------------------------ FUNCION: Convertir a datetime -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- convertir los datos de fechas en formato datetime

def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda

    Returns
    -------
    param_data : pandas.DataFrame : df modificado

    Debugging
    -------
    param_data = 'f_leer_archivo("archivo_tradeview_1.csv")
    """

    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    #

    return param_data





# -- ------------------------------------------------------------- FUNCION: Columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular los pips acumulados por operación, así como el profit acumulado.


def f_columnas_pips(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda,
                                después de haber ejecutado f_columnas_tiempos

    Returns
    -------
    param_data : pandas.DataFrame : df modificado

    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """

    datos['pips'] = [(datos.closeprice[i]-datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips'][datos.type=='sell'] *= -1
    datos['pips_acm'] = datos.pips.cumsum()
    datos['profit_acm'] = datos['profit'].cumsum()
    return datos.copy()



# -- ------------------------------------------------------ FUNCION: Estadisticas Básicas -- #

# -- ------------------------------------------------------------------------------------ -- #
# -- Calcula algunas estadísticas entre las operaciones generadas. 

def f_estadisticas_ba(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda,
                                después de haber ejecutado f_columnas_tiempos y f_columnas_pips

    Returns
    -------
    df_1_tabla : pandas.DataFrame : df con las estadísticas de comportamiento usando los datos presentados en el df.
    df_2_ranking : pandas.DataFrame : dataframe con ranking entre 0 y 1 de los activos con los cuales se ha sido más
                                    preciso en las operaciones realizadas.

    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """
    df_1_tabla = pd.DataFrame({
        'Ops totales': [len(datos['order']), 'Operaciones totales'],
        'Ganadoras': [len(datos[datos['pips_acm']>=0]), 'Operaciones ganadoras'],
        'Ganadoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de compra'],
        'Ganadoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de venta'],
        'Perdedoras': [len(datos[datos['pips_acm'] < 0]), 'Operaciones perdedoras'],
        'Perdedoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de compra'],
        'Perdedoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de venta'],
        'Mediana_profit': [datos['profit'].median(), 'Mediana de rendimeintos de las operaciones'],
        'Mediana_pips': [datos['pips_acm'].median(), 'Mediana de pips de las operaciones'],
        'r_efectividad': [len(datos[datos['pips_acm']>=0])/len(datos['order']),
                          'Ganadoras Totales/Operaciones Totales'],
        'r_proporcion': [len(datos[datos['pips_acm']>=0])/len(datos[datos['pips_acm'] < 0]),
                            'Ganadoras Totales/ Perdedoras Totales'],
        'r_efectividad_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)])/len(datos[datos['type']=='buy']),
                            'Ganadoras Compras/ Operaciones Totales'],
        'r_efectividad_v': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)])/len(datos[datos['type']=='sell']),
                            'Ganadoras Ventas/ Operaciones Totales']
    },index=['Valor', 'Descripcion'])


    tmp = pd.DataFrame({i: len(datos[datos.profit>0][datos.symbol == i])/len(datos[datos.symbol == i])
                      for i in datos.symbol.unique()}, index = ['rank']).T
    df_2_ranking = tmp.sort_values(by='rank', ascending=False).T

    return  {'df1' : df_1_tabla.copy(), 'df2': df_2_ranking.copy()}
    #   return df_1_tabla.copy(), df_2_ranking.copy() # prefiero hacer un return en tupla que en diccionario.
    #       Y recibir la tupla en dos variables distintas en el archivo main.py




# -- --------------------------------------------------------- FUNCION: Capital Acumulado -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Capital acumulado suponiendo que iniciamos con 5000

def f_capital_acm(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda,
                                después de haber ejecutado f_columnas_tiempos y f_columnas_pips

    Returns
    -------
    datos : pandas.DataFrame : se le añade una columna al dataframe recibido y se regresa el mismo dataframe modificado

    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """
    datos['capital_acm'] = datos.profit_acm + 5000
    return datos.copy()



# -- ------------------------------------------------------------- FUNCION: Profit diario -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- crea un dataframe con información de los rendimientos por día para calcularles MAD.

def f_profit_diario(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda,
                                después de haber ejecutado f_columnas_tiempos y f_columnas_pips

    Returns
    -------
    df_profit_diario : pandas.DataFrame : df con información de los rendimeintos por día.

    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """
    datos['ops'] = [i.date() for i in datos.closetime] # cantidad de operaciones cerradas ese dia
    diario = pd.date_range(datos.ops.min(),datos.ops.max()).date
    groups = datos.groupby('ops')
    profit = groups['profit'].sum()
    profit_diario = [profit[i] if i in profit.index else 0 for i in diario]
    df_profit_diario = pd.DataFrame(profit_diario,index = diario,columns = ['capital_acm']).cumsum()+5000
    return df_profit_diario



# -- --------------------------------------- FUNCION: Metricas de atribución al desempeño -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Crea matriz de metricas de atribución al desempeño

def f_estadisticas_mad(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de rendimientos diarios. debe contener columna 'capital_acm'

    Returns
    -------
    datos : pandas.DataFrame : Se regresa un dataframe con la información relevante acerca de los rendimientos
                                logarítmicos observados. Se calcularán los rendimientos tomando en cuenta la columna
                                de pips acumulados, de rendimientos acumulados y bajo el supuesto de que iniciamos con
                                5000 pesos en la cuenta.

    Debugging
    -------
    datos = f_daily_profit(f_leer_archivo("archivo_tradeview_1.csv"))
    """
    logrend = np.log(datos.capital_acm[1:].values/datos.capital_acm[:-1].values)

    rf = 0.0832 #tasa de rendimiento anual de s&p 500

    MAD = pd.DataFrame({
        'sharpe': (logrend.mean()*365-rf)/logrend.std()*(365**0.5),
        'sortino_c': (logrend.mean()*365-rf)/logrend[logrend>=0].std()*365**.5,
        'sortino_s': (logrend.mean()*365-rf)/logrend[logrend<0].std()*365**.5,
        'drawdown': datos.capital_acm.min()-5000,
        'drawup': datos.capital_acm.max()-5000,
        'information ratio': rf,
    }, index=['Valor'])

    return MAD

def f_sesgos_cognitivos(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de profit en transacciones. Tiene que tener columna 'profit'

    Returns
    -------
    df_markov : numpy.ndarray : df con la matriz de probabilidades de ganar/perder dinero dada la situación de perdida
                            o ganancia de la última transacción realizada.

    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")

    """
    def transition_matrix(transitions):
        trans = np.ones(transitions.shape)
        trans[transitions==False] = 0

        n = len(transitions.unique())  # number of states
        M = np.zeros((n,n))  # creates the empty Markov Matrix

        for (i, j) in zip(trans[:-1], trans[1:]):
            M[int(i),int(j)] += 1 # Dado i, se añade el acumulado de casos en el que el siguiente es j

        Mat = M.T / M.sum(axis=1)
        return Mat.T

    Markov = transition_matrix(datos.profit>0)
    df_markov = pd.DataFrame(Markov, columns=['lose', 'win'], index=['lose', 'win'])
    return df_markov

