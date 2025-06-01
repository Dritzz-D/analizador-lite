# test_validador.py

import pandas as pd
from agentes.validador_dataset import validar_dataframe

print("\n🧪 TEST 1: Dataset válido")
df_valido = pd.DataFrame({
    "edad": [30, 25, 22, 40, 36],
    "salario": [2000, 2500, 1800, 3000, 2700],
    "nombre": ["Ana", "Luis", "Juan", "Marta", "Pedro"]
})
resultado1 = validar_dataframe(df_valido)
print(resultado1)

print("\n🧪 TEST 2: Dataset con solo 1 columna numérica")
df_unica = pd.DataFrame({
    "edad": [30, 25, 22],
    "nombre": ["Ana", "Luis", "Juan"]
})
resultado2 = validar_dataframe(df_unica)
print(resultado2)

print("\n🧪 TEST 3: Dataset con columnas vacías o constantes")
df_malo = pd.DataFrame({
    "vacia": [None, None, None],
    "constante": [1, 1, 1],
    "texto": ["a", "b", "c"]
})
resultado3 = validar_dataframe(df_malo)
print(resultado3)
