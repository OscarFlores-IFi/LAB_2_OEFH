
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Francisco ME
# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

archivo = "archivo_tradeview_1.csv"
datos = fn.f_leer_archivo(archivo)

param_ins='usdjpy'
fn.f_pip_size(param_ins)
