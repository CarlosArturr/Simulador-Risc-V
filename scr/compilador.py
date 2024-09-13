import sys
      
def compilador(line, saida):

    byte = operacao(line)
    
    saida.write(f"{byte}\n")


def main():
    
    saida = open('binario.txt', 'w')
    risc = open( sys.argv[1] , 'r')

    for line in risc:
        retorno = retiraComentarios(line)
        
        if retorno != None:
            compilador(retorno, saida)


def retiraComentarios(line):
    indice = line.find("#")
    
    if indice == 0:
        return
    elif indice == -1:
        return line
    else:
        return line[:indice-1]


def operacao(line):
    instrucoes = line.split(" ") 
    instrucao = instrucoes[0].lower()
    code = ""

    if(instrucao == "add"):
        code = typeR(instrucoes, "0110011", "000", "0000000")
    elif(instrucao == "addi"):
        code = typeI(instrucoes, "0010011", "000")
    elif(instrucao == "sub"):
        code = "0b0110011"
    elif(instrucao == "or"):
        code = "0b0110011"
    elif(instrucao == "and"):
        code = "0b0110011"
    elif(instrucao == "andi"):
        code = "0b0010011"
    elif(instrucao == "beq"):
        code = "0b1100011"
    elif(instrucao == "bne"):
        code = "0b1100011"
    elif(instrucao == "jal"):
        code = "0b1101111"
    elif(instrucao == "ld"):
        code = "0b0000011"
    elif(instrucao == "sd"):
        code = "0b0100011"
    elif(instrucao == "nop"):
        code = "0b0b0010011"
        #addi x0, x0, x0 internamente
    else:
        code = "erro"
        
    return code

def typeR(intrucoes, code, fun3, fun7):
    #dec intruc rs2 rs1 rd
    
    code = "0b"+ fun7 + rs2 + rs1 + fun 3 + rd + code
    
    return code

"""""
def typeI(instrucoes, code, "000"):

def typeB():
    
def typeJ():

def typeS():
"""""
    

if __name__ == "__main__":
    main()
