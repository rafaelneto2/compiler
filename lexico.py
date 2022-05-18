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
    def __init__(self, linha, tipo, lexema, msg2=None):
        self.linha = linha
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        if msg2 is None:
            self.msg = msg
        else:
            self.msg = msg2
        self.lexema = lexema


class Lexico:
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
                    estado = 6
                elif car == '/' and self.proxChar() == '*':
                    estado = 7
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car == ':' and self.proxChar() == '=':
                    return Token(self.linha, TipoToken.ATRIB, car + self.getChar())
                elif car == '<' and self.proxChar() == '=':
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car == '>' and self.proxChar() == '=':
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car == '<' and self.proxChar() == '>':
                    return Token(self.linha, TipoToken.OPREL, car + self.getChar())
                elif car in {';', ':', ',', '(', ')', '{', '}', '=', '<', '>',
                             '+', '-', '*', '/', '!'}:
                    estado = 4
                elif car == '"':
                    estado = 5
                else:
                    return Token(self.linha, TipoToken.ERROR, '[' + car + ']', 'Caracter inválido' + car)

            elif estado == 2:
                # estado que trata identificadores e palavras reservada

                lexema = lexema + car
                car = self.getChar()

                if car is None or (not car.isalnum()):
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(self.linha, Lexico.reservadas[lexema], lexema)
                    else:
                        if len(lexema) > 16:
                            return Token(self.linha, TipoToken.ERROR, '[ identificador com mais de 16 dig. ]')
                        return Token(self.linha, TipoToken.ID, lexema)

            elif estado == 3:
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit()):
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
                    if car == '*' and self.getChar() == '/':
                        break
                if self.getChar() is None:
                    return Token(self.linha, TipoToken.ERROR, 'Bloco de comentário aberto e não fechado')
                estado = 1
