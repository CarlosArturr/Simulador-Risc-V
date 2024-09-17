import sys

run = 1
pc = 0
memoria = [0] * 128
registradores = [0] * 8

def simulador(binario):
    global run, pc
    
    limit = len(binario)
    
    while run == 1 and pc < limit:
        opcode = binario[pc][0]
        r = executa(binario[pc], opcode)
        pc_anterior = pc
        pc += 1
        
        print(f'pc = {pc_anterior}, opCode = {opcode}, Register r{r} = {registradores[r]}')
    
    print(f"PC final: {pc}")
    print(f"Registradores: {registradores}")

def executa(operacao, opcode):
    global run, registradores, pc
   
    if opcode == "0110011":  # add, sub, or, and
        opcode, rd, func3, rs1, rs2, func7 = operacao

        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)

        #Sem atribuicao
        if rd == 0:
            return rd
        #add
        elif func3 == "000" and func7 == "0000000":
            registradores[rd] = registradores[rs1] + registradores[rs2]
            return rd
        #sub
        elif func3 == "000" and func7 == "0100000":
            registradores[rd] = registradores[rs1] - registradores[rs2]
            return rd
        #and
        elif func3 == "111" and func7 == "0000000":
            registradores[rd] = registradores[rs1] & registradores[rs2]
            return rd
        #or
        elif func3 == "110" and func7 == "0000000":
            registradores[rd] = registradores[rs1] | registradores[rs2]
            return rd
        
    elif opcode == "0010011":  # addi, andi, nop
        opcode, rd, func3, rs1, imd = operacao

        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        imd = int(imd, 2)

        #Sem atribuicao
        if rd == 0:
            return rd
        #addi << nop
        elif func3 == "000":
            registradores[rd] = registradores[rs1] + imd
            return rd
        #andi
        elif func3 == "111":
            registradores[rd] = registradores[rs1] & imd
            return rd
    
    else:
        print("Opcode não reconhecido, finalizando simulação.")
        run = 0  # Finaliza o simulador se a instrução não for reconhecida.
        return 0
    """     
    elif opcode == "1100011":  # bne, beq
        opcode, offset, func3, rs1, rs2, offset2  = operacao
        #beq
        if func3 == "000":
            if(registradores[rs1] == registradores[rs2]):
                pc = 0
        #bne
        if func3 == "001":

       
    elif opcode == "1101111":  # jal
        opcode, rd, im8, im1, im10, imm1  = operacao


       
    elif opcode == "0100011":  # sd
        opcode, offset, func3, rs1, rs2, offset2  = operacao

       
    elif opcode == "0000011":  # ld
        opcode, rd, func3, rs1, imd = operacao
        
        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        imd = int(imd, 2)

        #Sem atribuicao
        if rd == 0:
            return rd
        elif func3 == "011":
            if rs1:
                registradores[rd] = memoria[rs1]
            if imd:
                registradores[rd] = memoria[imd]

"""

def lista(binario):
    lista_instrucao = []
    
    for line in binario:
        line = cleaner(line)
        opcode = line[25:32]
        lista_instrucao.append(organizaInstrucao(line, opcode))
        
    return lista_instrucao
        
def cleaner(line):
    line = line.split("b")
    return line[-1]

def organizaInstrucao(line, opcode):
    # Decodifica as instruções com base no opcode
    if opcode == "0110011":  # add, sub, or, and
        return [opcode, line[20:25], line[17:20], line[12:17], line[7:12], line[0:7]]
    elif opcode == "1100011":  # beq, bne
        return [opcode, line[24:25], line[20:24], line[17:20], line[12:17], line[7:12], line[1:7], line[0:1]]
    elif opcode == "1101111":  # jal
        return [opcode, line[20:25], line[12:20], line[11:12], line[1:11], line[0:1]]
    elif opcode == "0100011":  # sd
        return [opcode, line[20:25], line[17:20], line[12:17], line[7:12], line[0:7]]
    else:  # addi, andi, nop, ld
        return [opcode, line[20:25], line[17:20], line[12:17], line[0:12]]
        
def main():
    global run, pc, memoria, registradores
    
    binario = open(sys.argv[1], 'r')  # Arquivo com binário
    # Organiza instruções
    binario = lista(binario)
    
    # Executa simulador
    run = 1
    pc = 0
    memoria = [0] * 128
    registradores = [0] * 8
    
    simulador(binario)

if __name__ == "__main__":
    main()

