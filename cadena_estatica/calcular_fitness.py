from interprete_vf import ejecutar_bf
from interprete_vf import BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError


def fitness(deseado: str, obtenido: str, codigo: str, C: int = 10000) -> float:
    fitness = 0
    max_long = max(len(deseado), len(obtenido))
    
    for i in range(max_long):
        if i<len(deseado) and i<len(obtenido):
            d = ord(deseado[i])
            o = ord(obtenido[i])
            fitness += 256 - abs(d-o)*2
    
    if len(obtenido) > len(deseado):
        fitness = fitness * len(deseado)/len(obtenido)
        
    penalizacion = 1 / (1 + len(codigo)/C)
    
    return fitness * penalizacion


def evaluar_fitness(codigo: str, deseado: str) -> float:
    try:
        output = ejecutar_bf(codigo)
    except (BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError):
        return -1.0
    
    if output == '':
        return 0.0
    
    return round(fitness(deseado, output, codigo), 2)