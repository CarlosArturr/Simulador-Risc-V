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

