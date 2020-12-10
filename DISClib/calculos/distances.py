import math as m
import datetime

"""
Permite hacer cáculos de distancia en una superficie
esférica
"""

# ___________________________________________________
#  Funciones de cálculos
# ___________________________________________________

def calcularDistancia(radio, longitud, latitud):
    """
    Calcula la distancia entre dos lugares de una esfera
    """
    distancia = None
    factor_conversion = m.pi/180
    longitud = longitud*factor_conversion
    latitud = latitud*factor_conversion
    a = pow(m.sin(latitud/2),2) + m.cos(0)*m.cos(latitud)*pow(m.sin(longitud/2),2)
    c = 2*m.asin(m.sqrt(a))
    distancia = radio*c
    return distancia