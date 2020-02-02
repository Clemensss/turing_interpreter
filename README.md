# Interpretador de LFA
Interpretador de maquina de turing da aula do Paraguaçu

# Sintaxe

Bem parecida com a que ele deu, o que muda:

Pra definir uma subrotina (função) você usa:
	 

    DEFINE: <nome da sua funcao>
		COMANDOS
		COMANDOS
    HALT

As unicas coisas que precisam ser maiusculas sao DEFINE e HALT.

Também tem a funcao do MAIN, eh a mesma coisa q define so que sem nome 
personalizado, e ela precisa existir senao nao executa nada.
		
	MAIN: 
		COMANDOS
		COMANDOS
	HALT

Os comando preprogramados, eles sao:
		
	

    #comentarios com uma hash no comeco 
    #nao tem comentario na mesma linha q comandos
    #mas fora isso eh de boa
	
    #printar
    PRT: <caracter> 
    
    #scan e goto(ficam sempre na mesma linha)
    #goto comeca do zero
    SCAN: <caracter>, 0

    #move a fita pra direita
    DIR
	
    #move a fita pra esquerda
    ESQ 

Qualquer coisa tem o arquivo teste pra você ver como funciona.

## Utilização

Faz assim:
	

    python3 main.py <seu_arquivo>
