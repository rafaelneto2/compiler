import sintatico

if __name__ == "__main__":
    # nome = input("Entre com o nome do arquivo: ")
    nome = 'palavras\\exemplo2.txt'
    parser = sintatico.Sintatico()
    parser.interprete(nome)
