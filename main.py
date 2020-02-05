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
        if content[i] == "END":
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
        else:
            print("ERROR: {0} (line: {1}) not a defined keyword".format(lista[0], i))
            print(">>>> {}".format(':'.join(lista)))
            HALT()
            break
        
        if halt:
            break
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
    content = [x.strip() for x in content]
    content = [x for x in content if x[0] != '#']

    f.close()

    return make_subroutines(content) 
    
def print_fita():
    print(''.join(fita_turing))
    print(''.join([' ' for x in range(index)])+'^')
    
def print_dict(var):
    for x in var:
        print (x)
        for y in var[x]:
            print (y)

'''roda as funcoes ja preprogramadas'''
def run_preprogramed(content, name, i):

    inst = content[0]
    def exep_preprogramed():
        print("ERROR: Too many or too few arguments for {0} (line: {1}) in {2}".format(inst[0], i, name))
        print(">>>> {}".format(', '.join(content)))
        HALT()

    inst = inst.split(':')
    if inst[0] == "SCAN":
        if len(content) != 2:
            exep_preprogramed()

        if len(inst) != 2:
            exep_preprogramed()

        else:
            return SCAN(inst[1])

    elif inst[0] == "PRT":
        if len(content) != 1:
            exep_preprogramed()

        if len(inst) != 2:
            exep_preprogramed()

        else:
            PRT(inst[1])

    elif inst[0] == "DIR":
        if len(inst) > 1:
            exep_preprogramed()

        else:
            DIR()

    elif inst[0] == "ESQ":
        if len(inst) > 1:
            exep_preprogramed()

        else:
            ESQ()
    elif inst[0] == "HALT":
        HALT()

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
                print(">>>> {}".format(', '.join(inst)))
                HALT()
                break

        else:
            ver = run_preprogramed(inst, name, i)

        if halt:
            halt = False
            break

        if ver:
            i = int(inst[1])
        else:
            i+=1
        print_fita()
        if i == len(inst_l):
            break

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

def interactive():
    i = 0

    print("--- Interpretador de turing do Paragua ---")
    print("Made by yours truly (o retardado), Clemens Schrage\n")
    command_list = []
    cmd = True

    while True:
        ver = False 

        if not command_list:
            cmd = True

        if cmd:
            inst_l = input("{}>".format(i))
            inst_l = ''.join(inst_l.split())
            command_list.append(inst_l)
        else:
            inst_l = command_list[i]
            del command_list[i]

        inst = inst_l.split(",")
        ver = False

        if inst[0] == "EXIT":
            print("Exiting...")
            return

        if inst[0].split(':')[0] not in preprogramed:
            if inst[0] in subroutines: 
                run_sub(inst[0])
            else:
                print("\nERROR: Subroutine {1} (line: {0}) in {2} not defined\n".format(i, inst[0], "TERMINAL"))

        else:
            ver = run_preprogramed(inst, "TERMINAL", i)

        if ver:
            i = int(inst[1])
            cmd = False
        else:
            i+=1

        print_fita()


    print("Done")

def turing_main():
    if halt:
        print("EXECUTION NOT POSSIBLE")
    else:
        run_sub("MAIN")

def main():
    if len(sys.argv) < 2:
        interactive() 
    else:
        if sys.argv[1] == "-l":
            read_file(sys.argv[2])
            interactive()
        else:
            read_file(sys.argv[1])
            turing_main()

if __name__ == "__main__":
    main()
