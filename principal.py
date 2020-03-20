
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Oscar Flores
# -- repositorio: https://github.com/OscarFlores-IFi/LAB_2_OEFH
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

archivo = "archivo_tradeview_1.csv"
datos = fn.f_leer_archivo(archivo)
datos = fn.f_columnas_tiempos(datos)
datos = fn.f_columnas_pips(datos)
datos = fn.f_capital_acm(datos)
estadisticas = fn.f_estadisticas_ba(datos)
desempenio = fn.f_estadisticas_mad(datos)
sesgos = fn.f_sesgos_cognitivos(datos)
print(datos)
print(estadisticas['df1'])
print(estadisticas['df2'])
print(desempenio)
print(sesgos)



