import pytest
from calculadora import somar, dividir

def test_somar_numeros_positivos():
    assert somar (2,3) == 5

def test_somar_numeros_negativos():
    assert somar (-2, -3)  == -5

def test_dividir_normal():
    assert dividir (10,2) == 5

def test_dividir_numero_por_zero_lanca_erro():
    with pytest.raises(ValueError):
        dividir (10,0)