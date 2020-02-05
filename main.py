import sys

subroutines = dict()
fita_turing = ['#' for x in range(100)]
index = 0
preprogramed = ["SCAN", "PRT", "DIR", "ESQ", "HALT"]
halt = False
stop_exe = False


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
    global stop_exe
    i = 0
    while i < len(content):
        lista = content[i].split(':')

        if lista[0] == "DEFINE":
            i = add_new_sub(content, lista[1].strip(), i+1)
        elif lista[0] == "MAIN":
            i = add_new_sub(content, lista[0], i+1)
        else:
            exep_handle([], lista[0], i, "", "KEYWORD")
            break
        
        if stop_exe:
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


def exep_handle(cmd_list, cmd_name, line, sub_rot_name, ERROR):

    if ERROR == "ARGUMENTS":
        print("ERROR: Too many or too few arguments", end = " ")
        print("{0} (line: {1}) in {2}".format(cmd_name, line, sub_rot_name))

    elif ERROR == "SUB_NOT_DEFINED":
        print("ERROR: Subroutine {0} (line: {1}) in {2} not defined".format(cmd_name, line, sub_rot_name))

    elif ERROR == "KEYWORD":
        print("ERROR: {0} (line: {1}) not a defined keyword".format(cmd_name, line))

    print(">>>> {}".format(', '.join(cmd_list)))

    global stop_exe
    stop_exe = True

'''roda as funcoes ja preprogramadas'''
def run_preprogramed(cmd_line, sub_rot_name, exec_line):

    cmd_list = cmd_line.split(",")
    cmd = cmd_list[0].split(':')

    if cmd[0] not in preprogramed:
        exep_handle(cmd_list, cmd[0], exec_line, sub_rot_name, "SUB_NOT_DEFINED")

    if cmd[0] == "SCAN":
        if len(cmd_list) != 2 or len(cmd) != 2:
            exep_handle(cmd_list, cmd[0], exec_line, sub_rot_name, "ARGUMENTS")
        else:
            return SCAN(cmd[1])

    elif cmd[0] == "PRT":
        if len(cmd_list) != 1 or len(cmd) != 2:
            exep_handle(cmd_list, cmd[0], exec_line, sub_rot_name, "ARGUMENTS")

        else:
            PRT(cmd[1])

    elif cmd[0] == "DIR":
        if len(cmd) > 1:
            exep_handle(cmd_list, cmd[0], exec_line, sub_rot_name, "ARGUMENTS")

        else:
            DIR()

    elif cmd[0] == "ESQ":
        if len(cmd) > 1:
            exep_handle(cmd_list, cmd[0], exec_line, sub_rot_name, "ARGUMENTS")
        else:
            ESQ()

    elif cmd[0] == "HALT":
        HALT()

    return False

'''
   roda uma subrotina qualquer, se dentro da subrotina houver
   outra subrotina definida pelo usuario, a funcao eh chamada
   novo recursivamente, se for uma funcao preprogramada
   vai executar ela normalmente

   line eh o index de comandos, comeca de 0
'''
def exec_sub_loop(sub_name):
    list_commands = subroutines[sub_name]
    line = 0
    global halt

    while True:
        line = run_sub(list_commands[line], line, sub_name)

        print_fita()

        if halt:
            halt = False
            break

        if line >= len(list_commands):
            break

def run_sub(cmd, line, sub_name):

    if cmd in subroutines:
        exec_sub_loop(cmd)

    else:
        if run_preprogramed(cmd, sub_name, line):
            return int(cmd.split(",")[1])

    return line + 1


        

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
    line = 0

    print("--- Interpretador de turing do Paragua ---")
    print("Made by yours truly (o retardado), Clemens Schrage\n")
    command_list = []
    cmd = False

    while True:
        if command_list == []:
            cmd = False

        if not cmd:
            cmd_input = input("{0}>".format(line))
            cmd_input= ''.join(cmd_input.split())
            command_list.append(cmd_input)
        else:
            cmd_input = command_list[line]
            del command_list[line]

        if cmd_input == "EXIT":
            print("Exiting...")
            return

        line = run_sub(cmd_input, line, "TERMINAL")
        print_fita()

    print("Done")

def turing_main():
    if stop_exe:
        print("EXECUTION NOT POSSIBLE")
    else:
        exec_sub_loop("MAIN")

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
