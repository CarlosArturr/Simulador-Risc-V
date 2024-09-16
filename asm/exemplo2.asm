jal x2, save
loop:
    beq x15, x7, fim
    addi x15, x15, 1
    jal x0, loop
save:
    addi x15, x0, 1
    addi x6, x0, 2
    add x7, x15, x6
    jal x0, loop
fim:
    nop
