import sys

def add():
    
    
    
def compilador(line, saida):
    saida.write(f"{line}")


def retiraComentarios(line):
    indice = line.find("#")
    
    if indice == 0:
        return
    elif indice == -1:
        return line
    else:
        return line[:indice-1]
        

def main():
    
    saida = open('binario.txt', 'w')
    risc = open( sys.argv[1] , 'r')

    for line in risc:
        retorno = retiraComentarios(line)
        
        if retorno != None:
            compilador(retorno, saida)

if __name__ == "__main__":
    main()
  
        
