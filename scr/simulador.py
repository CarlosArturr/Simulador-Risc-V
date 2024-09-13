import sys

def simulador(pc):
    while run == 1:
        print("execute")    



def main():
    
    saida = open('operaçoes.txt', 'w')
    binario = open( sys.argv[1] , 'r')

    pc = 0
    run = 1
    simulador(pc, run)

if __name__ == "__main__":
        main()

