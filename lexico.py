# Nome Discente: Rafael Augusto de Rezende Neto
# Matrícula: 0021724
# Data: 23/05/2022

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.

# O arquivo lexico.py contém a implementação de um analisador léxico para a linguagem definida na especificação do
# trabalho prático. Foram implementadas as classes TipoToken, responsável pela definição dos tipos de tokens,
# Tokem, que representa uma TAD para um token encontrado e retornado, e, por fim,
# Lexico, responsável por abrir e fechar arquivo do programa (código de entrada) e resgatar os tokens através da função getToken().

# Referências bibliográficas:
# Exemplos enviados pelo professor da disciplina de Compiladores, Mário
# AHO, A. V. et al. Compiladores. 2 ed. São Paulo: Pearson Addison-Wesley, 2008.


from os import path


class TipoToken:
    ID = (1, 'id')
    CTE = (2, 'cte')  # numero
    CADEIA = (3, 'cadeia')
    PROGRAMA = (4, 'programa')
    VARIAVEIS = (5, 'variaveis')
    INTEIRO = (6, 'inteiro')
    REAL = (7, 'real')
    LOGICO = (8, 'logico')
    CARACTER = (9, 'caracter')
    SE = (10, 'se')
    SENAO = (11, 'senao')
    ENQUANTO = (12, 'enquanto')
    LEIA = (13, 'leia')
    ESCREVA = (14, 'escreva')
    FALSO = (15, 'falso')
    VERDADEIRO = (16, 'verdadeiro')
    ATRIB = (17, ':=')
    OPREL = (18, 'operadores-relacionais')
    OPAD = (19, 'operadores-adicao')
    OPMUL = (20, 'operadores-multiplicacao')
    OPNEG = (21, '!')
    PVIRG = (22, ';')
    DPONTOS = (24, ':')
    VIRG = (25, ',')
    ABREPAR = (26, '(')
    FECHAPAR = (27, ')')
    ABRECH = (28, '{')
    FECHACH = (29, '}')
    ERROR = (31, 'erro')
    FIMARQ = (32, 'fim-de-arquivo')


class Token:
    def __init__(self, linha, tipo, lexema, msg_erro=None):
        self.linha = linha
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        if msg_erro is None:
            self.msg = msg
        else:
            self.msg = msg_erro
        self.lexema = lexema


class Lexico:
    # variável global responsável por guardar linha do token
    global linha

    # dicionario de palavras reservadas
    reservadas = {
        'programa': TipoToken.PROGRAMA,
        'variaveis': TipoToken.VARIAVEIS,
        'inteiro': TipoToken.INTEIRO,
        'real': TipoToken.REAL,
        'logico': TipoToken.LOGICO,
        'caracter': TipoToken.CARACTER,
        'se': TipoToken.SE,
        'senao': TipoToken.SENAO,
        'enquanto': TipoToken.ENQUANTO,
        'leia': TipoToken.LEIA,
        'escreva': TipoToken.ESCREVA,
        'falso': TipoToken.FALSO,
        'verdadeiro': TipoToken.VERDADEIRO
    }

    def __init__(self, nomeArquivo):
        self.linha = 1
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # buffer de entrada
        self.buffer = ''

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)

            if c == '\n':
                self.linha = self.linha + 1

            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    # verifica qual é o próximo caracter
    def proxChar(self):
        c = self.getChar()
        self.ungetChar(c)
        return c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while True:
            if estado == 1:
                # estado 1 é responsável pela primeira classificação
                car = self.getChar()
                if car is None:
                    return Token(self.linha, TipoToken.FIMARQ, 'fda')
                elif car in {' ', '\t', '\n'}:
                    pass
                elif car == '/' and self.proxChar() == '/':
                    # Estado 6 é responsável pelos comentários de linha
                    estado = 6
                elif car == '/' and self.proxChar() == '*':
                    # Estado 7 é responsável pelos comentários de bloco
                    estado = 7
                elif car.isalpha():
                    # Estado 2 é responsável pelos caracteres do alfabeto (idetificadores e palavras reservadas)
                    estado = 2
                elif car.isdigit():
                    # Estado 3 é responsável pelas constantes numéricas inteiras
                    estado = 3
                elif car == ':' and self.proxChar() == '=':
                    # Verifica se é uma atribuição e retorna
                    return Token(self.linha, TipoToken.ATRIB, car + self.getChar())
                elif car == '<' and self.proxChar() == '=':
                    # Verifica se é uma operação de menor igual e retorna
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car == '>' and self.proxChar() == '=':
                    # Verifica se é uma operação de maior e retorna
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car == '<' and self.proxChar() == '>':
                    # Verifica se é uma operação de diferente e retorna
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car in {';', ':', ',', '(', ')', '{', '}', '=', '<', '>',
                             '+', '-', '*', '/', '!'}:
                    # Estado 4 é responsável pelos caracteres especiais
                    estado = 4
                elif car == '"':
                    # Estado 5 é responsável pelas cadeias
                    estado = 5
                else:
                    # caracter inválido identificado
                    return Token(self.linha, TipoToken.ERROR, '[' + car + ']', 'Caracter inválido: ' + car)

            elif estado == 2:
                # estado que trata identificadores e palavras reservada

                lexema = lexema + car
                car = self.getChar()

                if car is None or (not car.isalnum()):
                    self.ungetChar(car)

                    # verifica se lexema é uma palavra reservada
                    if lexema in Lexico.reservadas:
                        return Token(self.linha, Lexico.reservadas[lexema], lexema)
                    else:
                        # verifica se identificador tem mais de 16 caracteres
                        if len(lexema) > 16:
                            return Token(self.linha, TipoToken.ERROR, lexema, '[ identificador com mais de 16 dig. ]')
                        return Token(self.linha, TipoToken.ID, lexema)

            elif estado == 3:
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit() and car != '.'):
                    self.ungetChar(car)
                    return Token(self.linha, TipoToken.CTE, lexema)

            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if lexema == '!':
                    return Token(self.linha, TipoToken.OPNEG, lexema)
                elif lexema == ';':
                    return Token(self.linha, TipoToken.PVIRG, lexema)
                elif lexema == ':':
                    return Token(self.linha, TipoToken.DPONTOS, lexema)
                elif lexema == ',':
                    return Token(self.linha, TipoToken.VIRG, lexema)
                elif lexema == '(':
                    return Token(self.linha, TipoToken.ABREPAR, lexema)
                elif lexema == ')':
                    return Token(self.linha, TipoToken.FECHAPAR, lexema)
                elif lexema == '{':
                    return Token(self.linha, TipoToken.ABRECH, lexema)
                elif lexema == '}':
                    return Token(self.linha, TipoToken.FECHACH, lexema)
                elif lexema == '=':
                    return Token(self.linha, TipoToken.OPREL, lexema)
                elif lexema == '>':
                    return Token(self.linha, TipoToken.OPREL, lexema)
                elif lexema == '<':
                    return Token(self.linha, TipoToken.OPREL, lexema)
                elif lexema == '+':
                    return Token(self.linha, TipoToken.OPAD, lexema)
                elif lexema == '-':
                    return Token(self.linha, TipoToken.OPAD, lexema)
                elif lexema == '*':
                    return Token(self.linha, TipoToken.OPMUL, lexema)
                elif lexema == '/':
                    return Token(self.linha, TipoToken.OPMUL, lexema)

            elif estado == 5:
                lexema = lexema + car
                car = self.getChar()
                lexema = lexema + car
                while (not car is None) and (car != '"'):
                    car = self.getChar()
                    if car is None:
                        return Token(self.linha, TipoToken.ERROR, lexema, '[ cadeia não fechada ]')
                    lexema = lexema + car
                return Token(self.linha, TipoToken.CADEIA, lexema)

            elif estado == 6:
                # consome comentário de linha
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                estado = 1

            elif estado == 7:
                # consome comentário de bloco
                while not car is None:
                    car = self.getChar()
                    if car == '*' and self.proxChar() == '/':
                        break
                if self.getChar() is None:
                    return Token(self.linha, TipoToken.ERROR, None, 'Bloco de comentário aberto e não fechado')
                estado = 1
