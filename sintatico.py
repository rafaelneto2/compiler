# Nome Discente: Rafael Augusto de Rezende Neto
# Matrícula: 0021724
# Data: 23/05/2022

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.

# O arquivo sintatico.py contém a implementação de um analisador sintatico para a linguagem definida pela gramatica
# contida na especificação do trabalho prático. Foi implementada a classe Sintatico, responsável pela análise
# sintatica do complilador, com uma função interprete() que recebe o nome do arquivo e é responsável por iniciar o processo,
# a função consome() é responsável por consumir os terminais da gramatica e verificar a existência de erros.

# Referências bibliográficas:
# Exemplos enviados pelo professor Mário
# AHO, A. V. et al. Compiladores. 2 ed. São Paulo: Pearson Addison-Wesley, 2008.


from lexico import TipoToken as tt, Lexico


class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.erros = []
        # buffer de token
        self.buffer = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            # inicia execução a partir da produção inicial
            self.PROG()
            self.consome(tt.FIMARQ)

            self.lex.fechaArquivo()

            # exibe todos erros encontrados
            if len(self.erros) > 0:
                for erro in self.erros:
                    print(erro)

    def atualIgual(self, token):
        try:
            (const, msg) = token
        except:
            const = token.const
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual(token):
            # se buffer não for nulo, consome token do buffer
            if self.buffer is not None:
                self.tokenAtual = self.buffer
                self.buffer = None
            else:
                self.tokenAtual = self.proxToken()
        else:
            (const, msg) = token

            # erro sintático encontrado
            self.erros.append('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"' % (
                self.tokenAtual.linha, msg, self.tokenAtual.lexema))

            # pega próximo token
            prox = self.proxToken()
            if const == prox.const:
                # se próximo token é igual ao atual, então ignora token inválido e continua execusão
                self.tokenAtual = self.proxToken()
            else:
                # senão, guarda token em um buffer, para ser reutilizado
                self.buffer = prox

    def PROG(self):
        self.consome(tt.PROGRAMA)
        self.consome(tt.ID)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.atualIgual(tt.VARIAVEIS):
            self.consome(tt.VARIAVEIS)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def D(self):
        if self.atualIgual(tt.ID):
            self.LIST_DECLS()
        else:
            pass

    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PVIRG)

    def LIST_ID(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID()
        else:
            pass

    def TIPO(self):
        if self.atualIgual(tt.INTEIRO):
            self.consome(tt.INTEIRO)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.LOGICO):
            self.consome(tt.LOGICO)
        elif self.atualIgual(tt.CARACTER):
            self.consome(tt.CARACTER)
        else:
            self.erros.append('ERRO DE SINTAXE [linha %d]: Era esperado um tipo.' % (
                self.tokenAtual.linha))

    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):
        if self.atualIgual(tt.SE) \
                or self.atualIgual(tt.ENQUANTO) \
                or self.atualIgual(tt.LEIA) \
                or self.atualIgual(tt.ESCREVA) \
                or self.atualIgual(tt.ID):
            self.LISTA_COMANDOS()

    def COMANDOS(self):
        if self.atualIgual(tt.SE):
            self.IF()
        elif self.atualIgual(tt.ENQUANTO):
            self.WHILE()
        elif self.atualIgual(tt.LEIA):
            self.READ()
        elif self.atualIgual(tt.ESCREVA):
            self.WRITE()
        elif self.atualIgual(tt.ID):
            self.ATRIB()
        else:
            self.erros.append('ERRO DE SINTAXE [linha %d]: COMANDOS não encontrados' % (
                self.tokenAtual.linha))

    def IF(self):
        self.consome(tt.SE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.atualIgual(tt.SENAO):
            self.consome(tt.SENAO)
            self.C_COMP()
        else:
            self.erros.append('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"' % (
                self.tokenAtual.linha, tt.SENAO[1], self.tokenAtual.lexema))
            self.C_COMP()

    def WHILE(self):
        self.consome(tt.ENQUANTO)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()

    def READ(self):
        self.consome(tt.LEIA)
        self.consome(tt.ABREPAR)
        self.LIST_ID()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def ATRIB(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)

    def WRITE(self):
        self.consome(tt.ESCREVA)
        self.consome(tt.ABREPAR)
        self.LIST_W()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            self.EXPR()

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    def FAT(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.atualIgual(tt.VERDADEIRO):
            self.consome(tt.VERDADEIRO)
        elif self.atualIgual(tt.FALSO):
            self.consome(tt.FALSO)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()
        else:
            self.erros.append('ERRO DE SINTAXE [linha %d]: Sem argumentos' % (
                self.tokenAtual.linha))

    def proxToken(self):

        # recebe próximo token
        new_token = self.lex.getToken()

        if new_token.tipo == tt.ERROR:
            # erro léxico encontrado
            self.erros.append('ERRO LÉXICO [linha %d]: %s' % (
                new_token.linha, new_token.msg))

            # segue execusão (método pânico)
            return self.proxToken()
        else:
            # retorna token caso não tenha erro
            return new_token
