
STEP_LIMIT = 10000

class BrainfuckSyntaxError(Exception):
    """ Error de sintaxis: los corchetes se encuentran mal balanceados"""
    pass

class BrainfuckRunError(Exception):
    """ Error de ejecución: el puntero se encuentra fuera de rango"""
    pass

class BrainfuckStepLimitError(Exception):
    """ Error de ejecución: se ha superado el límite de pasos (posible existencia de bucle infinito)"""
    pass


def prefijar_saltos(prog: list[str]) -> dict:
    """
    Genera un diccionario con los saltos entre corchetes [ y ].
    
    El diccionario mapea cada Ã­ndice de corchete de apertura a su cierre
    y viceversa. Si un corchete no tiene pareja (huÃ©rfano), su valor es None.
    
    """
    
    pila = []
    saltos = {}
    for i, t in enumerate(prog):
        if t == '[':
            pila.append(i)
            
        elif t == ']':
            if not pila:
                saltos[i] = None
            else:
                j = pila.pop()
                saltos[i] = j
                saltos[j] = i
                
    for j in pila:
        saltos[j] = None
        
    return saltos


def ejecutar_bf(prog: str, entrada:str  = "") -> str:
    """
    Ejecuta un programa Brainfuck y devuelve su salida.

    Comportamiento respecto a corchetes huérfanos:
        * ']' huérfano -> se ignora.
        * '[' huérfano con celda == 0 -> intenta saltar; si no hay cierre, se ignora.
        * '[' huérfano con celda != 0 -> se ignora.
    """
    
    programa = list(prog)
    saltos = prefijar_saltos(programa)

    cinta = [0]
    i = j = num_pasos = 0
    salida = []
    entrada_idx = 0          

    n = len(programa)

    while i < n:
        num_pasos += 1
        if num_pasos > STEP_LIMIT:
            raise BrainfuckStepLimitError("se ha superado el límite de pasos")

        instr = programa[i]

        if instr == '>':
            j += 1
            if j == len(cinta):
                cinta.append(0)

        elif instr == '<':
            j -= 1
            if j < 0:
                raise BrainfuckRunError("El puntero se encuentra fuera de rango")

        elif instr == '+':
            cinta[j] = (cinta[j] + 1) % 256

        elif instr == '-':
            cinta[j] = (cinta[j] - 1) % 256
            
        elif instr == '.':
            salida.append(chr(cinta[j]))
            
        elif instr == ',':
            if entrada_idx < len(entrada):
                cinta[j] = ord(entrada[entrada_idx])
                entrada_idx += 1
            else: 
                cinta[j] = 0        

        elif instr == '[':
            if cinta[j] == 0:
                pareja = saltos.get(i, None)
                if pareja is not None:
                    i = pareja
                else:
                    pass
                
        elif instr == ']':
            pareja = saltos.get(i, None)
            if pareja is None:
                pass
            elif cinta[j] != 0:
                i = pareja
                
        i += 1

    return "".join(salida)

