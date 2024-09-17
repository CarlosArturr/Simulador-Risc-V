# Inicializa registradores com valores imediatos usando addi
addi x0, x0, 56    # x2 = 56
addi x2, x0, 9    # x2 = 9
addi x3, x0, 55   # x3 = 55
# Inicializa x1 com 4
addi x1, x0, 4    # x1 = 4
# Inicializa x3 com 3
addi x3, x0, 3    # x3 = 3

# Operações com add e sub
add x4, x2, x1    # x4 = x2 + x1 (x4 = 9 + 4 = 13)
sub x5, x3, x1    # x5 = x3 - x1 (x5 = 3 - 4 = -1)

# Operações lógicas AND e OR
and x6, x2, x3    # x6 = x2 AND x3 (bitwise AND)
or x7, x2, x3     # x7 = x2 OR x3 (bitwise OR)

# Operação lógica com valor imediato usando ANDI
andi x1, x2, 7    # x8 = x2 AND 7 (bitwise AND com valor imediato)

# Instrução NOP (sem operação, apenas para preenchimento)
nop               # Não faz nada

# Resultado final armazenado em x8