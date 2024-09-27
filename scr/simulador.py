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
        pc_anterior = pc
        r = executa(binario[pc], opcode)
        pc += 1
        
        if(run == 1):
            print(f'pc = {pc_anterior}, opCode = {opcode}, Register r{r} = {registradores[r]}')
        else:
            print("Opcode não reconhecido, finalizando simulação.")
    
    print(f"PC final: {pc-1}")
    print(f"Registradores: {registradores}")
    print(f"Memoria: {memoria}")

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
        imd = complemento2(imd)

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
    
    elif opcode == "0000011":  # ld
        opcode, rd, func3, rs1, imd = operacao
        #imd inutilizado pois e tratado diretamento por registrador
        
        rd = int(rd, 2)
        rs1 = int(rs1, 2)

        #Sem atribuicao
        if rd == 0:
            return rd
        elif func3 == "011":
            if rs1:
                registradores[rd] = memoria[registradores[rs1]]
                return rd

    elif opcode == "0100011":  # sd
        opcode, offset, func3, rs1, rs2, offset2  = operacao
        #ofsset inutilizado pois e tratado diretamento por registrador
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        
        if func3 == "000":
            memoria[rs2] = registradores[rs1]
            #corrigir
            return rs1
    
    elif opcode == "1100011":  # bne, beq
        opcode, im, offset, func3, rs1, rs2, offset2, imm  = operacao
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        offset = complemento2(im + offset)
        offset2 = complemento2(imm + offset2)
        pulo = (offset + offset2)
        
        #beq
        if func3 == "000":
            if(registradores[rs1] == registradores[rs2]):
                pc = pc + pulo
              
        #bne
        if func3 == "001":
            if(registradores[rs1] != registradores[rs2]):
                pc = pc + pulo
        
        print(pulo)
        return 0              
       
    elif opcode == "1101111":  # jal
        opcode, rd, im8, im, im10, imm  = operacao
        rd = int(rd, 2)
        
        im8 = complemento2(im + im8)
        im10 = complemento2(imm + im10)
        
        pulo = (im8 + im10)
        
        print(pulo)
        pc = pc + pulo
        return rd
        
    else:
        run = 0  # Finaliza o simulador se a instrução não for reconhecida.
        return 0

def complemento2(binario):
    if binario[0] == '1':
        invertido = ''.join('1' if b == '0' else '0' for b in binario)
        decimal = int(invertido, 2) + 1
        decimal = -decimal
    else:
        decimal = int(binario, 2) 
    return decimal

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