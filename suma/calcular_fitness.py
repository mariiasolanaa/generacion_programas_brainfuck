from interprete_vf import ejecutar_bf
from interprete_vf import BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError


def fitness(valor_obtenido: int, valor_deseado: int, codigo: str, caracteres_extra: int, C: int = 1000) -> float:
    
    error = abs(valor_obtenido - valor_deseado)
    penalizacion_basura = caracteres_extra * 50
    
    score = 256 - error*3 - penalizacion_basura
    fitness = max(0, score)
    penalizacion = 1 / (1 + len(codigo) / C)
    
    return fitness * penalizacion


def evaluar_fitness(codigo: str, lista_casos: list[tuple[int, int]]) -> float:
    fitness_total = 0.0
    
    for a, b in lista_casos:
        objetivo = a + b
        entrada_cod = chr(a) + chr(b)
        
        try:
            salida_real = ejecutar_bf(codigo, entrada=entrada_cod)
            
            if len(salida_real) == 0:
                valor_obt = objetivo + 256       # Error máximo forzado
                extras = 0
            else:
                valor_obt = ord(salida_real[0])  # Tomamos el valor del primero
                extras = len(salida_real) - 1    # Calculamos cuántos sobran

        except (BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError):
            valor_obt = objetivo + 256
            extras = 10                          # Castigo extra por crashear
            
        fitness_total += fitness(valor_obt, objetivo, codigo, extras)
        
    return round(fitness_total, 2)