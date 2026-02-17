from primera_generacion import generar_char
from interprete_vf import prefijar_saltos
import random


# VAMOS A DEFINIR TODAS LAS POSIBLES MUTACIONES

ESQUELETOS = [
    '[-]',          # Reset celda
    '[->+<]',       # Mover a derecha
    '[->+>+<<]',    # Mover a dos celdas
    '[->+++++<]',   # Multiplicar
]

def mutacion_insertar_esqueleto(prog: str) -> str:
    # Inserta un bloque funcional completo una sola vez
    pos = random.randrange(len(prog) + 1)
    esqueleto = random.choice(ESQUELETOS)
    return prog[:pos] + esqueleto + prog[pos:]

def mutacion_reemplazo(prog: str) -> str:
    #la longitud del codigo se mantiene igual
    prog_mutado = list(prog) # Convertimos a lista para facilitar reemplazos
    num_cambios = random.randint(1, 3)
    for _ in range(num_cambios):
        n = len(prog_mutado)
        if n > 0:
            pos = random.randrange(n)
            nuevo_char = generar_char()
            prog_mutado[pos] = nuevo_char
    return "".join(prog_mutado)

def mutacion_insercion(prog: str) -> str:
    #la longitud del codigo se aumenta x unidades, con 1<=x<=5
    prog_mutado = prog
    num_inserciones = random.randint(1, 3)
    for _ in range(num_inserciones):
        pos = random.randrange(len(prog_mutado) + 1)
        nuevo_char = generar_char()
        prog_mutado = prog_mutado[:pos] + nuevo_char + prog_mutado[pos:]
    return prog_mutado

def mutacion_borrado(prog: str) -> str:
    #la longitud del codigo disminuye en una unidad
    if len(prog) <= 2: 
        return prog
    pos = random.randrange(len(prog))
    return prog[:pos] + prog[pos+1:]

def mutacion_intercambio1(prog: str) -> str:
    #la longitud del codigo se mantiene igual
    n = len(prog)
    if n < 2:
        return prog
    i,j = random.sample(range(n),2)
    char = prog[i]
    sin_char = prog[:i] + prog[i+1:]
    return sin_char[:j] + char + sin_char[j:]

def mutacion_intercambio2(prog: str) -> str:
    #la longitud del codigo se mantiene igual
    n = len(prog)
    if n < 2:
        return prog
    i,j = random.sample(range(n),2)
    lista = list(prog)
    lista[i], lista[j] = lista[j], lista[i]
    return "".join(lista)

MUTACIONES = [
    (mutacion_reemplazo,          0.15),
    (mutacion_insercion,          0.20),
    (mutacion_borrado,            0.20),
    (mutacion_intercambio1,       0.15),
    (mutacion_intercambio2,       0.15),
    (mutacion_insertar_esqueleto, 0.15),
]

def elegir_mutacion():
    mutaciones = [f for (f,p) in MUTACIONES]
    probabilidad = [p for (f,p) in MUTACIONES]
    return random.choices(mutaciones, weights = probabilidad, k=1)[0]



# VAMOS A DEFINIR TODOS LOS POSIBLES BUCLES

def encontrar_bucles(prog: str) -> list[tuple[int, int]]:
    # Devuelve una lista de tuplas (inicio, fin) de los bucles externos
    saltos = prefijar_saltos(prog) 
    bucles = []
    i = 0
    while i < len(prog):
        if prog[i] == '[':
            fin = saltos[i]
            if fin is not None:
                bucles.append((i, fin))
                i = fin  # Saltamos al final del bucle
        i += 1
    return bucles

def cruce_intercambio_bucles(prog1: str, prog2: str) -> tuple[str, str]:
    bucles1 = encontrar_bucles(prog1)
    bucles2 = encontrar_bucles(prog2)
    
    # Si alguno no tiene bucles, recurrimos a cruce de un punto
    if not bucles1 or not bucles2:
        return cruce_un_punto(prog1, prog2)
    
    # Elegimos un bucle al azar de cada padre
    b1_start, b1_end = random.choice(bucles1)
    b2_start, b2_end = random.choice(bucles2)
    
    parte1 = prog1[b1_start : b1_end + 1]
    parte2 = prog2[b2_start : b2_end + 1]
    
    hijo1 = prog1[:b1_start] + parte2 + prog1[b1_end+1:]
    hijo2 = prog2[:b2_start] + parte1 + prog2[b2_end+1:]
    
    return hijo1, hijo2

def cruce_un_punto(prog1: str, prog2: str) -> tuple[str, str]:
    min_long = min(len(prog1), len(prog2))
    if min_long < 4:
        return prog1, prog2
    c = random.randint(1, min_long-1)       #para asegurarnos de que no va a haber rangos vacíos
    hijo1 = prog1[:c] + prog2[c:]
    hijo2 = prog2[:c] + prog1[c:]
    return hijo1, hijo2

def cruce_dos_puntos(prog1: str, prog2: str) -> tuple[str, str]:
    min_long = min(len(prog1), len(prog2))
    if min_long < 3:
        # Si son muy cortos, no podemos cruzarlos por 2 puntos.
        # Los devolvemos tal cual
        return prog1, prog2
    c1, c2 = random.sample(range(1, min_long), 2)
    if c2<c1:
        c1, c2 = c2, c1
    hijo1 = prog1[:c1] + prog2[c1:c2] + prog1[c2:]
    hijo2 = prog2[:c1] + prog1[c1:c2] + prog2[c2:]
    return hijo1, hijo2

def cruce_uniforme(prog1: str, prog2: str) -> tuple[str, str]:
    hijo1 = []
    hijo2 = []
    for a,b in zip(prog1, prog2):
        if random.random() < 0.5:
            hijo1.append(a)
            hijo2.append(b)
        else:
            hijo1.append(b)
            hijo2.append(a)
    return ''.join(hijo1), ''.join(hijo2)

CRUCES = [
    (cruce_un_punto,           0.25),
    (cruce_dos_puntos,         0.20),
    (cruce_uniforme,           0.5),
    (cruce_intercambio_bucles, 0.50)
]

def elegir_cruce():
    cruces = [f for (f,p) in CRUCES]
    probabilidad = [p for (f,p) in CRUCES]
    return random.choices(cruces, weights = probabilidad, k=1)[0]
    