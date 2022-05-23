# Nome Discente: Rafael Augusto de Rezende Neto
# Matrícula: 0021724
# Data: 23/05/2022

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.

# O arquivo main.py é resposável por resgatar os parâmetros de entrada, e inicar o complilador.

# Referências bibliográficas:
# Exemplos enviados pelo professor Mário
# AHO, A. V. et al. Compiladores. 2 ed. São Paulo: Pearson Addison-Wesley, 2008.


import sys

import sintatico

if __name__ == "__main__":
    # nome = input("Entre com o nome do arquivo: ")
    nome = sys.argv[1]
    # nome = 'palavras\\exemplo3.txt'
    parser = sintatico.Sintatico()
    parser.interprete(nome)
