import sys
import os

rotulos = {}
contLine = 0

def main():

    entrada = sys.argv[1]
    nome_saida = os.path.splitext(entrada) [0] + '.txt'
    
    saida = open(nome_saida, 'w')
    risc = open(entrada, 'r')

    cont = 0 
    for line in risc:
        global rotulos
        retorno = retiraComentarios(line)
        
        if retorno != None:
            if(retorno.strip()[-1] == ":"):
                rotulos[retorno.strip()[:-1]] = cont
                cont -= 1
                
            cont += 1
    
    print(rotulos)
    risc.seek(0)
     
    
    for line in risc:
        retorno = retiraComentarios(line)
        
        if retorno != None:
            compilador(retorno, saida)


    saida.close()
    risc.close()
            
def compilador(line, saida):
    line = line.strip()
    byte = operacao(line)
    
    if(byte != ""):
        saida.write(f"{byte}\n")

def retiraComentarios(line):
    indice = line.find("#")
    
    if indice == 0:
        return
    elif indice == -1:
        return line
    else:
        return line[:indice-1]
    

def operacao(line):
    instrucoes = line.split(" ", 1) 
    opcode = instrucoes[0].lower()
    
    if len(instrucoes) != 1:
        operandos = instrucoes[1].split(", ")
        

    if(opcode == "add"):
        byte = typeR(operandos, "0110011", "000", "0000000")
    elif(opcode == "addi"):
        byte = typeI(operandos, "0010011", "000")
    elif(opcode == "sub"):
        byte = typeR(operandos, "0110011", "000", "0100000")
    elif(opcode == "or"):
        byte = typeR(operandos, "0110011", "110", "0000000")
    elif(opcode == "and"):
        byte = typeR(operandos, "0110011", "111", "0000000")
    elif(opcode == "andi"):
        byte = typeI(operandos, "0010011", "111")
    elif(opcode == "beq"):
        byte = typeB(operandos, "1100011", "000")
    elif(opcode == "bne"):
        byte = byte = typeB(operandos, "1100011", "001")
    elif(opcode == "jal"):
        byte = typeJ(operandos, "1101111")
    elif(opcode == "ld"):
        byte = typeI(operandos, "0000011" ,"011")
    elif(opcode == "sd"):
        byte = typeS(operandos, "0100011", "000")
    elif(opcode == "nop"):
        byte = typeI(["x0", "x0", "0"], "0010011", "000")
    else:
        byte = ""
        
    return byte

def typeR(operandos, code, fun3, fun7):
    rd, rs1, rs2 = filtra_registradores("r", operandos)
    return f"0b{fun7}{rs2}{rs1}{fun3}{rd}{code}"

def typeI(operandos, code, fun3):
    rd, rs1, imd = filtra_registradores("i", operandos)
    return f"0b{imd}{rs1}{fun3}{rd}{code}"

def typeB(operandos, code, func3):
    rs1, rs2, imd = filtra_registradores("b", operandos)

    # Separar o offset para os bits específicos
    offset = int(imd, 2)
    offset12 = (offset >> 12) & 1
    offset10_5 = (offset >> 5) & 0x3F  # 6 bits
    offset4_1 = (offset >> 1) & 0xF   # 4 bits
    offset11 = (offset >> 11) & 1
    
    return f"0b{offset12:01b}{offset10_5:06b}{rs2}{rs1}{func3}{offset4_1:04b}{offset11:01b}{code}"
    
def typeJ(operandos, code):
    rd, imd = filtra_registradores("j", operandos)

    # Separar o offset para os bits específicos
    offset = int(imd, 2)
    offset20 = (offset >> 20) & 1
    offset10_1 = (offset >> 1) & 0x3FF  # 10 bits
    offset11 = (offset >> 11) & 1
    offset19_12 = (offset >> 12) & 0xFF  # 8 bits
    
    return f"0b{offset20:01b}{offset10_1:010b}{offset11:01b}{offset19_12:08b}{rd}{code}"

def typeS(operandos, code, func3):
    rs1, rs2, imd = filtra_registradores("s", operandos)
    
    # Separar o offset para os bits específicos
    offset = int(imd, 2)
    offset11_5 = (offset >> 11) & 0x7F 
    
    return f"0b{offset11_5:07b}{rs2}{rs1}{func3}{offset4_0:05b}{code}"

def filtra_registradores(tipo, operandos):
    resultado = []
    global rotulos 
    global contLine
    
    for elem in operandos:
        if(elem[0] == "x"):
            resultado.append(filtra_reg(elem))
        else:
            try:
                resultado.append(filtra_immI(elem))
            except:
                if elem in rotulos:
                    if tipo == "s":
                        resultado.append(f"{(rotulos[elem]- contLine):07b}")
                    elif tipo == "b":
                        print(f"Valor do rotulo: {rotulos[elem]}")
                        print(f"Valor do cont: {contLine}")
                        print(rotulos[elem]- contLine)
                        resultado.append(f"{(rotulos[elem]- contLine):012b}")
                    else:
                        print(f"Valor do rotulo: {rotulos[elem]}")
                        print(f"Valor do cont: {contLine}")
                        print(rotulos[elem]- contLine)
                        resultado.append(f"{(rotulos[elem]- contLine):020b}")
    print(contLine)
    print(operandos)
    contLine += 1

    
    return resultado

def filtra_reg(operando):
    return f"{int(operando[1:]):05b}"
    
    
def filtra_immI(elem):
    return f"{int(elem):012b}"


if __name__ == "__main__":
    main()
    