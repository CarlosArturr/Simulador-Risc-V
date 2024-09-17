#Armazena o N a x2, N está em 1024 na memória
ld  x2, x1024
#Amazenando a posicao de Memoria Para a recursão
addi x1, x0, 1
#Aumentando para n+1
add x2, x2, x1
#Inicializando Resultado
addi x3, x0, 1



soma:   
    beq  x1, x2,  exit
    add  x3, x3, x1
    addi x1, x1, 1
    beq x0, x0, soma
       
#Resulato em 2000 na memoria
exit:   sd   x3, x2000
