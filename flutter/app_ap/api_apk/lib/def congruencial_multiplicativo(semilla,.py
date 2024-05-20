def congruencial_multiplicativo(semilla, a, M):
    numeros_generados = [semilla]
    x_actual = semilla
    
    while True:
        x_siguiente = (a * x_actual) % M
        
        if x_siguiente in numeros_generados:
            break  # Se encontró una repetición, salir del bucle
            
        numeros_generados.append(x_siguiente)
        x_actual = x_siguiente
    
    return numeros_generados

# Semilla, multiplicador y módulo dados
semilla = 1
a = 11
M = 154

# Generar la serie
serie_generada = congruencial_multiplicativo(semilla, a, M)

# Mostrar la serie generada
print("Serie generada:", serie_generada)