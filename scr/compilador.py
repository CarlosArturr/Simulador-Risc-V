import sys

def main():
    
    saida = open('binario.txt', 'w')
    risc = open( sys.argv[1] , 'r')

    for line in risc:
        retorno = retiraComentarios(line)
        
        if retorno != None:
            compilador(retorno, saida)
            
def compilador(line, saida):
    line = line.strip()
    byte = operacao(line)
    
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
        byte = "0b0110011"
    elif(opcode == "or"):
        byte = "0b0110011"
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
    elif(opcode[-1] == ":"):
        byte = opcode
    else:
        byte = ""
        
    return byte

def typeR(operandos, code, fun3, fun7):
    #dec intruc rs2 rs1 rd
    rs2 = "10001"
    rs1 = "10001"
    rd = "10001"
    return "0b"+ fun7 + rs2 + rs1 + fun3 + rd + code

def typeI(operandos, code, fun3):
    #dec imd rs1
    imd = "100000000001"
    rs1 = "10001"
    rd = "10001"
    return "0b" + imd + rs1 + fun3 + rd + code

def typeB(operandos, code, func3):
    #dec rs1 rs2 e ofssets
    rs2 = "10001"
    rs1 = "10001"
    ofsset12 = "101"
    ofsset4 = "101"
    return "0b" + ofsset12 + rs2 + rs1 + func3 + ofsset4 + code
    
def typeJ(operandos, code):
    #dec rs1 ofset
    rs1 = "10001"
    ofsset = "100000000001"
    
    return "0b" + ofsset + rs1 + code

def typeS(operandos, code , func3):
    #dec rs1 rs2 e ofssets
    rs2 = "10001"
    rs1 = "10001"
    ofsset11 = "101"
    ofsset4 =  "101"
    return "0b" + ofsset11 + rs2 + rs1 + func3 + ofsset4 + code


if __name__ == "__main__":
    main()

def filtra_registradores(tipo, operandos):
    resultado = []
    
    for elem in operandos:
        if(elem[0] == "x"):
            resultado.append(filtra_reg(elem))
        else:
            resultado.append(filtra_imm(tipo, elem))
    
    return resultado

def filtra_reg(operando):
    return f"{int(operando[1:]):05b}"
    
    
def filtra_imm(tipo, elem):
    if tipo == "i":
        return f"{int(elem):012b}" 
    elif tipo == "s":
        return f"{int(elem):07b}" 
    elif tipo == "b":
        return f"{int(elem):012b}" 
    else:
        return f"{int(elem):020b}" 
