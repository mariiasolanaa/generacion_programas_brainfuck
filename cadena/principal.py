#PROGRAMA PRINCIPAL PARA DEVOLVER UNA CADENA DADA COMO ENTRADA
import random

from interprete_vf import ejecutar_bf
from interprete_vf import BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError
from calcular_fitness import evaluar_fitness
from primera_generacion import generar_poblacion_inicial
from mutaciones_y_cruces import elegir_mutacion, elegir_cruce
from criterios_seleccion import seleccion_elite, seleccion_torneo


def generaciones(casos_prueba: list[tuple[str, str]], tamaño_poblacion: int = 100, 
                 tamaño_programa: int = 20, max_generaciones: int = 1000, prob_cruce: float = 0.4, 
                 fraccion_elite: float = 0.02, tamaño_torneo: int = 2) -> tuple [str | None, float]:
    
    sol_encontrada = False
    poblacion = generar_poblacion_inicial(tamaño_poblacion, tamaño_programa)
    num_generacion = 1
    
    mejor_prog_global = None
    mejor_fitness_global = -1
    
    while not sol_encontrada:
    #while (num_generacion <= max_generaciones and not sol_encontrada):
        
        fitnesses = [evaluar_fitness(prog, casos_prueba) for prog in poblacion]
        
        indice_mejor = max(range(tamaño_poblacion), key = lambda i: fitnesses[i])
        mejor_prog = poblacion[indice_mejor]
        mejor_fitness = fitnesses[indice_mejor]
        
        #Para visualizar, ejecutamos el primer caso de prueba
        try:
            ejemplo_entrada = casos_prueba[0][0]
            ejemplo_salida = ejecutar_bf(mejor_prog, entrada = ejemplo_entrada)
        except (BrainfuckSyntaxError, BrainfuckRunError, BrainfuckStepLimitError):
            ejemplo_salida = ''
            
        print(f"Generacion: {num_generacion}  |  fitness: {mejor_fitness}  |  salida[{ejemplo_entrada}]: {ejemplo_salida}")
        
        if mejor_fitness > mejor_fitness_global:
            mejor_fitness_global = mejor_fitness
            mejor_prog_global = mejor_prog
            
        #Comprobamos que el programa cumple TODOS los casos de prueba correctamente
        exito_total = True
        for entrada, deseada in casos_prueba:
            try:
                obtenida = ejecutar_bf(mejor_prog, entrada = entrada)
                if obtenida != deseada:
                    exito_total = False
            except:
                exito_total = False
                
        if exito_total:
            sol_encontrada = True
            print(f"Objetivo alcanzado en la generacion {num_generacion}")
            return mejor_prog, mejor_fitness
        
        # Construimos la siguiente generación
        elite = seleccion_elite(poblacion, fitnesses, fraccion_elite = fraccion_elite)
        nueva_poblacion = elite[:]
        programas_vistos = set(nueva_poblacion)
        
        while len(nueva_poblacion) < tamaño_poblacion:
            r = random.random()
            
            # CRUCES
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
                
            # MUTACION
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
    return mejor_prog_global, mejor_fitness_global


#PRUEBAS
#generaciones([('maria', 'maria'), ('luis', 'luis')])
#generaciones([('maria', 'maria'), ('luis', 'luis'), ('bea', 'bea')])
#generaciones([('maria', 'maria'), ('luis', 'luis'), ('bea', 'bea'), ('s', 's')])
#generaciones([('maria', 'maria'), ('magnolia', 'magnolia'), ('bea', 'bea'), ('s', 's'), ('', '')])
        