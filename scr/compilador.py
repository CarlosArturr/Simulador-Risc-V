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
                
            cont += 1
                   
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
    return "0b"+ fun7 + rs2 + rs1 + fun3 + rd + code

def typeI(operandos, code, fun3):
    rd, rs1, imd = filtra_registradores("i", operandos)
    return "0b" + imd + rs1 + fun3 + rd + code

def typeB(operandos, code, func3):
    #dec rs1 rs2 e ofssets
    rs1, rs2, imd = filtra_registradores("b", operandos)
    
    ofsset12 = "101"
    ofsset4 = "101"
    return "0b" + ofsset12 + rs2 + rs1 + func3 + ofsset4 + code
    
def typeJ(operandos, code):
    #dec rs1 ofset
    rs1, ofsset = filtra_registradores("i", operandos)
    
    return "0b" + ofsset + rs1 + code

def typeS(operandos, code , func3):
    #dec rs1 rs2 e ofssets
    rs1, rs2 = filtra_registradores("s", operandos)
    ofsset11 = "101"
    ofsset4 =  "101"
    return "0b" + ofsset11 + rs2 + rs1 + func3 + ofsset4 + code


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
    