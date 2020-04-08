
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Oscar Flores
# -- repositorio: https://github.com/OscarFlores-IFi/LAB_2_OEFH
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vz

archivo = "archivo_tradeview_1.csv"
datos = fn.f_leer_archivo(archivo)
datos = fn.f_columnas_tiempos(datos)
datos = fn.f_columnas_pips(datos)
datos = fn.f_capital_acm(datos)
estadisticas = fn.f_estadisticas_ba(datos)
vz.plot_ranking(estadisticas['df2'])
profit_diario = fn.f_profit_diario(datos)
desempenio = fn.f_estadisticas_mad(profit_diario)
sesgos = fn.f_sesgos_cognitivos1(datos)
df1 = estadisticas['df1']
df2 = estadisticas['df2']
sesgos2 = fn.f_sesgos_cognitivos2(datos,profit_diario)
print(sesgos2)








