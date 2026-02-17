#PROGRAMA PRINCIPAL
import random

from interprete_vf import ejecutar_bf
from interprete_vf import BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError
from calcular_fitness import evaluar_fitness
from primera_generacion import generar_poblacion_inicial
from mutaciones_y_cruces import elegir_mutacion, elegir_cruce
from criterios_seleccion import seleccion_elite, seleccion_torneo


def generaciones(deseado: str, tamaño_poblacion: int = 100, tamaño_programa: int = 70, 
                 max_generaciones: int = 200, prob_cruce: float = 0.4, 
                 fraccion_elite: float = 0.02, tamaño_torneo: int = 2) -> tuple [str | None, str, float]:
    
    sol_encontrada = False
    poblacion = generar_poblacion_inicial(tamaño_poblacion, tamaño_programa)
    num_generacion = 1
    
    mejor_prog_global = None
    mejor_salida_global = ''
    mejor_fitness_global = -1
    
    while not sol_encontrada:
    #while (num_generacion <= max_generaciones and not sol_encontrada):
        fitnesses = [evaluar_fitness(prog, deseado) for prog in poblacion]
        
        indice_mejor = max(range(tamaño_poblacion), key = lambda i: fitnesses[i])
        mejor_prog = poblacion[indice_mejor]
        mejor_fitness = fitnesses[indice_mejor]
        
        try:
            mejor_salida = ejecutar_bf(mejor_prog)
        except (BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError):
            mejor_salida = ''
            
        print(f"Generacion: {num_generacion}  |  fitness: {mejor_fitness}  |  salida: {mejor_salida}")
        
        # Actualizamos el mejor global si procede
        if mejor_fitness > mejor_fitness_global:
            mejor_fitness_global = mejor_fitness
            mejor_prog_global = mejor_prog
            mejor_salida_global = mejor_salida
            
        # Comprobamos si alcanzamos el objetivo exacto
        if mejor_salida == deseado:
            sol_encontrada = True
            print(f"Objetivo alcanzado en la generacion {num_generacion}")
            return mejor_prog, mejor_salida, mejor_fitness
        
        # Construimos la siguiente generación
        elite = seleccion_elite(poblacion, fitnesses, fraccion_elite = fraccion_elite)
        nueva_poblacion = elite[:]
        programas_vistos = set(nueva_poblacion)
        
        while len(nueva_poblacion) < tamaño_poblacion:
            r = random.random()
            
            # CRUCE
            if r < prob_cruce and len(nueva_poblacion) <= tamaño_poblacion -2:
                padres = seleccion_torneo(poblacion, fitnesses, k=2, tamaño_torneo = tamaño_torneo)
                cruce = elegir_cruce()
                hijo1, hijo2 = cruce(padres[0], padres[1])
                
                if hijo1 not in programas_vistos:
                    nueva_poblacion.append(hijo1)
                    programas_vistos.add(hijo1)
                
                if hijo2 not in programas_vistos:
                        nueva_poblacion.append(hijo2)
                        programas_vistos.add(hijo2)
                        
            # MUTACIÓN    
            else:
                padre = seleccion_torneo(poblacion, fitnesses, k=1, tamaño_torneo = tamaño_torneo)[0]
                mutacion = elegir_mutacion()
                hijo = mutacion(padre)
                
                if hijo not in programas_vistos:
                    nueva_poblacion.append(hijo)
                    programas_vistos.add(hijo)
                
        poblacion = nueva_poblacion
        num_generacion += 1
        
    print("No se ha conseguido la salida esperada")
    return mejor_prog_global, mejor_salida_global, mejor_fitness_global
        