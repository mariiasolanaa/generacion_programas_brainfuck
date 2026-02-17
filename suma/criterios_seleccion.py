import random


def seleccion_torneo(poblacion: list[str], fitnesses: list[float], tamaño_torneo: int = 2, k: int = 1) -> list[str]:
    n = len(poblacion)
    seleccionados = []
    
    for _ in range(k):
        indices = random.sample(range(n), tamaño_torneo)
        mejor_indice = max(indices, key = lambda i : fitnesses[i])
        seleccionados.append(poblacion[mejor_indice])
        
    return seleccionados


def seleccion_elite(poblacion: list[str], fitnesses: list[float], fraccion_elite: float = 0.02) -> list[str]:
    n = len(poblacion)
    num_elite = max(1, int(fraccion_elite * n))
    
    indices_ordenados = sorted(range(n), key = lambda i: fitnesses[i], reverse = True)   #para ordenar los menores fitnesses primero
    elite = [poblacion[i] for i in indices_ordenados[:num_elite]]
    
    return elite