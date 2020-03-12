
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Francisco ME
# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd




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
    return




# -- ------------------------------------------------------ FUNCION: Convertir a datetime -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- convertir los datos de fechas en formato datetime

def f_columnas_tiempos(param_data):
    """
    Parameters:

    param_data : str : nombre del archivo a leer.

    Return : pd DataFrame :

    Debugging
    --------
    param_data = datos
    """

    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    #

    return param_data




# -- ------------------------------------------------------------ FUNCION: Columnas Pips --- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Calcula los pips acumulados y el profit acumulado. 

def f_columnas_pips(datos):
    datos['pips_acm'] = [(datos.closeprice[i]-datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips_acm'][datos.type=='sell'] *= -1
    datos['profit_acm'] = datos['profit'].cumsum()
    return datos


# -- ------------------------------------------------------ FUNCION: Estadísticas básicas -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Calcula algunas estadísticas entre las operaciones generadas. 

def f_estadisticas_ba(datos):
    return pd.DataFrame({
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
                          'Operaciones Totales Vs Ganadoras Totales'],
        'r_proporcion': [len(datos[datos['pips_acm']>=0])/len(datos[datos['pips_acm'] < 0]),
                            'Ganadoras Totales Vs Perdedoras Totales'],
        'r_efectividad_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)])/len(datos['order']),
                            'Totales Vs Ganadoras Compras'],
        'r_efectividad_v': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)])/len(datos['order']),
                            'Totales Vs Ganadoras Ventas']


    })


