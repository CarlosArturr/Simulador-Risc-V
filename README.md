# Simulador Risc-V

Este projeto faz parte de uma disciplina de Organização e Arquitetura de Computadores (OAC), com o objetivo de construir um simulador baseado na arquitetura RISC-V, utilizando um subconjunto de instruções. O simulador é capaz de interpretar e executar instruções como add, addi, and, andi, beq, bne, jal, ld, nop, or, sd, sub.
Pelos Alunos:

    Carlos Artur
    Débora Sabrina
    Nicolas Paz
    João Pedro

Parte 1:

Mais detalhes sobre o projeto podem ser encontrados na primeira parte da documentação, disponível em Parte 1 do Projeto.

Compilador

O compilador deste projeto recebe um arquivo de entrada em formato .asm (com as instruções em Assembly RISC-V) e gera um arquivo de saída .txt, com o mesmo nome, contendo o código binário correspondente.
Como Usar

    Execução: Para rodar o compilador, execute o seguinte comando no terminal:

    bash

python montador.py <arquivo_de_entrada>

O arquivo de entrada <arquivo_de_entrada> deve conter as instruções em Assembly, e a saída será gerada automaticamente com o mesmo nome, mas com a extensão .txt.

Exemplo: Se você tiver um arquivo de entrada chamado programa.asm, o comando seria:

bash

    python montador.py programa.asm

    Isso gerará um arquivo de saída chamado programa.txt com o código binário correspondente.

Funcionalidades

    Instruções Suportadas:
        Aritméticas: add, addi, sub
        Lógicas: and, andi, or
        Controle de fluxo: beq, bne, jal
        Memória: ld, sd
        Outras: nop

    Rotulagem: O compilador identifica rótulos no código e os traduz para endereços de memória apropriados, permitindo saltos condicionais e incondicionais.

    Comentários: Linhas ou trechos de linhas iniciados com # são ignorados pelo compilador.

Estrutura do Código

    main(): Função principal que gerencia a leitura do arquivo de entrada, a remoção de comentários e a tradução das instruções.
    compilador(): Converte as instruções para seu formato binário adequado, chamando funções específicas para cada tipo de instrução.
    typeR(), typeI(), typeS(), typeB(), typeJ(): Geram o código binário para os diferentes formatos de instrução suportados pela arquitetura RISC-V.
    filtra_registradores(): Processa os operandos das instruções, convertendo-os em valores binários.

Referências

    Guia Prático RISC-V 1.0.0
    Especificação RISC-V v2.2
    Arquitetura e Organização de Computadores (William Stallings)
    Digital Design and Computer Architecture (David Harris, Sarah Harris)

    Links:

    http://riscvbook.com/portuguese/guia-pratico-risc-v-1.0.0.pdf
    https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf
    https://archive.org/details/stallings-arquitetura-e-organizacao-de-computadores-10a/page/n31/mode/2up?view=theater 

