import sys
import os


def main():
    entrada = sys.argv[1]
    nome_saida = os.path.splitext(entrada)[0] + '.txt'
    
    # Primeiro passe para identificar os rótulos e armazenar as instruções
    labels = {}
    instr_lines = []
    
    with open(entrada, 'r') as risc:
        for line_number, line in enumerate(risc):
            retorno = retiraComentarios(line)
            if retorno:
                if ':' in retorno:
                    label = retorno.split(':')[0].strip()
                    labels[label] = len(instr_lines)  # Armazenar o índice da instrução
                else:
                    instr_lines.append(retorno.strip())

    # Segundo passe para processar as instruções com rótulos já conhecidos
    with open(nome_saida, 'w') as saida:
        for line in instr_lines:
            byte = processarInstrucao(line, labels, instr_lines)
            saida.write(f"{byte}\n")

def retiraComentarios(line):
    indice = line.find("#")
    if indice == 0:
        return None
    elif indice == -1:
        return line
    else:
        return line[:indice].strip()

def processarInstrucao(instrucao, labels, instr_lines):
    partes = instrucao.split(" ", 1)
    opcode = partes[0].lower()
    operandos = partes[1].split(", ") if len(partes) > 1 else []

    if opcode == "add":
        byte = typeR(operandos, "0110011", "000", "0000000")
    elif opcode == "addi":
        byte = typeI(operandos, "0010011", "000")
    elif opcode == "sub":
        byte = typeR(operandos, "0110011", "000", "0100000")
    elif opcode == "or":
        byte = typeR(operandos, "0110011", "110", "0000000")
    elif opcode == "and":
        byte = typeR(operandos, "0110011", "111", "0000000")
    elif opcode == "andi":
        byte = typeI(operandos, "0010011", "111")
    elif opcode == "beq":
        byte = typeB(operandos, "1100011", "000", labels, instr_lines)
    elif opcode == "bne":
        byte = typeB(operandos, "1100011", "001", labels, instr_lines)
    elif opcode == "jal":
        byte = typeJ(operandos, "1101111", labels, instr_lines)
    elif opcode == "ld":
        byte = typeI(operandos, "0000011", "011")
    elif opcode == "sd":
        byte = typeS(operandos, "0100011", "000")
    elif opcode == "nop":
        byte = typeI(["x0", "x0", "0"], "0010011", "000")
    else:
        byte = ""
    
    # Garantir que o byte tenha exatamente 32 bits
    return byte.zfill(34)  # Adiciona zeros à esquerda para garantir 32 bits

def typeR(operandos, code, fun3, fun7):
    rd, rs1, rs2 = filtraRegistradores("r", operandos)
    return "0b" + fun7 + rs2 + rs1 + fun3 + rd + code

def typeI(operandos, code, fun3):
    rd, rs1, imd = filtraRegistradores("i", operandos)
    return "0b" + imd + rs1 + fun3 + rd + code

def typeB(operandos, code, func3, labels, instr_lines):
    rs1, rs2, target_label = filtraRegistradores("b", operandos)
    if target_label in labels:
        target_index = labels[target_label]
        current_index = instr_lines.index(' '.join([operandos[0]] + operandos[1:]))
        offset = target_index - current_index - 1
        # Ajustar para valores negativos usando complemento de dois e garantir 12 bits
        offset = (offset & 0xFFF)  # Garantir que o offset esteja dentro de 12 bits
        offset_bin = f"{offset:012b}"
    else:
        offset_bin = "000000000000"  # Rótulo não encontrado (deve ser ajustado conforme necessário)

    return "0b" + offset_bin + rs2 + rs1 + func3 + "000000" + code



def typeJ(operandos, code, labels, instr_lines):
    rd, target_label = filtraRegistradores("j", operandos)
    if target_label in labels:
        target_index = labels[target_label]
        current_index = instr_lines.index(f"jal {', '.join(operandos[1:])}")
        offset = target_index - current_index - 1
        # Ajustar para valores negativos usando complemento de dois e garantir 20 bits
        offset = (offset & 0xFFFFF)  # Garantir que o offset esteja dentro de 20 bits
        offset_bin = f"{offset:020b}"
    else:
        offset_bin = "00000000000000000000"  # Rótulo não encontrado (deve ser ajustado conforme necessário)

    return "0b" + offset_bin + rd + code

def typeS(operandos, code, func3):
    rs1, rs2 = filtraRegistradores("s", operandos)
    offset = "000000000000"  # Ajustar conforme necessário
    return "0b" + offset + rs2 + rs1 + func3 + "0000000" + code

def filtraRegistradores(tipo, operandos):
    resultado = []
    for elem in operandos:
        if elem[0] == "x":
            resultado.append(filtra_reg(elem))
        else:
            try:
                resultado.append(filtra_imm(tipo, elem))
            except:
                resultado.append("0")  # Aqui é quando encontra um imediato que vai para um rótulo
    return resultado

def filtra_reg(operando):
    return f"{int(operando[1:]):05b}"

def filtra_imm(tipo, elem):
    if tipo == "i":
        return f"{int(elem):012b}" 
    elif tipo == "b":
        return f"{int(elem):012b}" 
    elif tipo == "j":
        return f"{int(elem):020b}"
    elif tipo == "s":
        return f"{int(elem):012b}"
    return "000000000000"

if __name__ == "__main__":
    main()

"""
//Simulador:

import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python simulador.py <arquivo_de_instrucoes>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Inicialização das memórias e registradores
    inst_mem = [0] * 128  # Memória de instruções com capacidade de 128 endereços
    data_mem = [0] * 16   # Memória de dados com capacidade de 16 endereços
    registers = [0] * 8   # Registradores r0 a r7
    pc = 0  # Program Counter

    # Carregar instruções do arquivo de entrada
    try:
        with open(arquivo_entrada, 'r') as file:
            for i, line in enumerate(file):
                if i < 128:  # Limitar a 128 instruções
                    inst_mem[i] = int(line.strip(), 2)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        sys.exit(1)
    except ValueError:
        print("Erro: O arquivo de entrada contém valores que não são binários válidos.")
        sys.exit(1)

    def decode_and_execute(instr):
        # Decodificar a instrução
        opcode = instr & 0b1111111
        rd = (instr >> 7) & 0b11111
        rs1 = (instr >> 15) & 0b11111
        rs2 = (instr >> 20) & 0b11111
        funct3 = (instr >> 12) & 0b111
        funct7 = (instr >> 25) & 0b1111111
        imm = (instr >> 20) & 0b111111111111

        # Executar a instrução com base no opcode e outros campos
        if opcode == 0b0110011:  # R-type
            if funct3 == 0b000 and funct7 == 0b0000000:  # ADD
                registers[rd] = registers[rs1] + registers[rs2]
            elif funct3 == 0b000 and funct7 == 0b0100000:  # SUB
                registers[rd] = registers[rs1] - registers[rs2]
            elif funct3 == 0b111 and funct7 == 0b0000000:  # AND
                registers[rd] = registers[rs1] & registers[rs2]
            elif funct3 == 0b110 and funct7 == 0b0000000:  # OR
                registers[rd] = registers[rs1] | registers[rs2]
            else:
                raise ValueError("Instrução R-Type inválida")
        elif opcode == 0b0010011:  # I-type
            if funct3 == 0b000:  # ADDI
                registers[rd] = registers[rs1] + imm
            elif funct3 == 0b111:  # ANDI
                registers[rd] = registers[rs1] & imm
            elif funct3 == 0b110:  # ORI
                registers[rd] = registers[rs1] | imm
            else:
                raise ValueError("Instrução I-Type inválida")
        elif opcode == 0b1100011:  # B-Type
            if funct3 == 0b000:  # BEQ
                if registers[rs1] == registers[rs2]:
                    return pc + imm
            elif funct3 == 0b001:  # BNE
                if registers[rs1] != registers[rs2]:
                    return pc + imm
            else:
                raise ValueError("Instrução B-Type inválida")
        elif opcode == 0b1101111:  # J-Type
            if funct3 == 0b000:  # JAL
                registers[rd] = pc + 4
                return pc + imm
            else:
                raise ValueError("Instrução J-Type inválida")
        elif opcode == 0b0000011:  # Load
            if funct3 == 0b011:  # LD
                registers[rd] = data_mem[registers[rs1] + imm]
            else:
                raise ValueError("Instrução Load inválida")
        elif opcode == 0b0100011:  # Store
            if funct3 == 0b000:  # SD
                data_mem[registers[rs1] + imm] = registers[rs2]
            else:
                raise ValueError("Instrução Store inválida")
        elif opcode == 0b1110011:  # NOP
            pass
        else:
            raise ValueError("Opcode inválido")
        
        return None

    # Simulação
    while pc < 128:
        instr = inst_mem[pc]
        if instr == 0b00000000000000000000000000000000:
            # Instrução inválida, encerrar
            break
        next_pc = decode_and_execute(instr)
        if next_pc is not None:
            pc = next_pc
        else:
            pc += 1

    # Exibir o estado final dos registradores e da memória
    print(f"pc={pc},", end="")
    print(f"r0={registers[0]},r1={registers[1]},r2={registers[2]},r3={registers[3]},r4={registers[4]},r5={registers[5]},r6={registers[6]},r7={registers[7]}")
    
    print("Memória de Dados:")
    for i in range(len(data_mem)):
        print(f"endereço {i}: {data_mem[i]}")

if __name__ == "__main__":
    main()

"""