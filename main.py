import sys

subroutines = dict()
fita_turing = ['#' for x in range(100)]
index = 0
preprogramed = ["SCAN", "PRT", "DIR", "ESQ", "HALT"]
halt = False


'''
    tira todos os espacos e salva o o comando na sub_list,
    depois de ler HALT manda a lista de comandos para o dicionario
    de subrotinas
'''

def add_new_sub(content, sub_name, i):
    sub_list = []
    while True:
        if content[i] == "HALT":
            break
        sub_list.append(''.join(content[i].split()))
        i+=1

    subroutines[sub_name] = sub_list

    return i            

'''
    pega a lista de strings content e procura pelas
    palavras chave DEFINE e MAIN, se acha uma das 
    duas define uma subrotina com todos os comandos
    entre ela e HALT
'''
def make_subroutines(content):

    i = 0
    while i < len(content):
        lista = content[i].split(':')

        if lista[0] == "DEFINE":
            i = add_new_sub(content, lista[1].strip(), i+1)
        elif lista[0] == "MAIN":
            i = add_new_sub(content, lista[0], i+1)
        
        i+=1

'''
    le o arquivo e separa ele por cada linha, ja tirando o
    \n, depois faz uma limpeza em cada linha, pra tirar
    linhas vazias e depois uma pra tirar todos os whitespaces
'''
def read_file(file_name):

    f = open(file_name, "r")

    content = f.read().splitlines()
    content = [x for x in content if x.strip()]
    content = [x for x in content if x[0] != '#']
    content = [x.strip() for x in content]

    print(content)
    f.close()

    make_subroutines(content) 
    
def print_fita():
    print(''.join(fita_turing))
    print(''.join([' ' for x in range(index)])+'^')
    
def print_dict(var):
    for x in var:
        print (x)
        for y in var[x]:
            print (y)

'''roda as funcoes ja preprogramadas'''
def run_preprogramed(inst, name):

    inst = inst.split(':')
    if inst[0] == "SCAN":
        if len(inst) != 2:
            print("ERROR: Too many or too few arguments for SCAN in {}".format(name[:-1]))
            HALT()
        else:
            return SCAN(inst[1])

    elif inst[0] == "PRT":
        if len(inst) != 2:
            print("ERROR: Too many or too few arguments for PRT in {}".format(name[:-1]))
            HALT()
        else:
            PRT(inst[1])
            return False

    elif inst[0] == "DIR":
        DIR()
        return False

    elif inst[0] == "ESQ":
        ESQ()
        return False
'''
   roda uma subrotina qualquer, se dentro da subrotina houver
   outra subrotina definida pelo usuario, a funcao e chamada de
   novo recursivamente, se for uma funcao preprogramada
   vai executar ela normalmente

   i eh o index de comandos, comeca de 0
'''
def run_sub(name):
    inst_l = subroutines[name]
    i = 0
    global halt

    while True:
        inst = inst_l[i].split(",")
        ver = False

        if inst[0].split(':')[0] not in preprogramed:
            if inst[0] in subroutines: 
                run_sub(inst[0])
            else:
                print("ERROR: Subroutine {1} (line: {0}) in {2} not defined".format(i, inst[0], name[:-1]))
                break

        else:
            ver = run_preprogramed(inst[0], name)

        if ver:
            i = int(inst[1])
        else:
            i+=1
        print_fita()
        if i == len(inst_l):
            break
                
    print(''.join(fita_turing))

def SCAN(char):
    global index
    if char == fita_turing[index]:
        return True
    else:
        return False

def PRT(char):
    fita_turing[index] = char

def HALT():
    global halt
    halt = True

def DIR():
    global index
    global fita_turing
    index += 1
    if index == len(fita_turing):
        fita_turing = fita_turing + ['#' for x in range(100)]

def ESQ():
    global index
    if index != 0:
        index -= 1

def turing():
    run_sub("MAIN")

def main():
    read_file(sys.argv[1])

    turing()

if __name__ == "__main__":
    main()
