import sys

def compilador(line):
    saida.write(f"0b00000000000000000000000000000000\n")














saida = open('binario.txt', 'w')

risc = open( sys.argv[1] , 'r')

for line in risc:
    compilador(line)

