from interprete_vf import ejecutar_bf
from interprete_vf import BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError


def fitness(deseado: str, obtenido: str, codigo: str, C: int = 10000) -> float:
    fitness = 0
    min_long = min(len(deseado), len(obtenido))
    
    for i in range(min_long):
        d = ord(deseado[i])
        o = ord(obtenido[i])
        fitness += 256 - abs(d-o)*2
    
    if len(obtenido) > len(deseado):
        fitness = fitness * len(deseado)/len(obtenido)
    
    penalizacion = 1 / (1 + len(codigo)/C)
    
    return fitness * penalizacion


def evaluar_fitness(codigo: str, casos_prueba: list[tuple[str, str]]) -> float:
    fitness_total = 0.0
    for entrada, salida_esperada in casos_prueba:
        try:
            salida_obtenida = ejecutar_bf(codigo, entrada = entrada)
        except (BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError):
            return -1.0
        fitness_total += fitness(salida_esperada, salida_obtenida, codigo)
        
    return round(fitness_total, 2)
        