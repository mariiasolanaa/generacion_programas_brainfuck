import random

ALFABETO = {
    '+' : 0.20,
    '-' : 0.20,
    '>' : 0.10,
    '<' : 0.10,
    '.' : 0.15,
    ',' : 0.0,
    '[' : 0.125,
    ']' : 0.125,
}

INSTRUCCIONES: list[str] = list(ALFABETO.keys())
PORCENTAJES: list[float] = list(ALFABETO.values())

def generar_char() -> str:
    return random.choices(INSTRUCCIONES, weights = PORCENTAJES, k=1)[0]

def generar_programa(n: int) -> str:
    codigo = "".join(random.choices(INSTRUCCIONES, weights = PORCENTAJES, k=n))
    return codigo

def generar_poblacion_inicial(num_individuos: int, longitud_programa: int) -> list[str]:
    poblacion = []
    for _ in range(num_individuos):
        programa = generar_programa(longitud_programa)
        poblacion.append(programa)
    return poblacion