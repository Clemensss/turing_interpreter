# Interpretador de LFA
Interpretador de maquina de turing da aula do Paraguaçu

# Sintaxe

Bem parecida com a que ele deu, o que muda:

Pra definir uma subrotina (função) você usa:
	 

    DEFINE: <nome da sua funcao>
		COMANDOS
		COMANDOS
    END

As unicas coisas que precisam ser maiusculas sao DEFINE e END.

Também tem a funcao do MAIN, eh a mesma coisa q DEFINE so que sem nome 
personalizado, e ela precisa existir nada executa.
		
	MAIN: 
		COMANDOS
		COMANDOS
	END

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

    #para o programa
    HALT

Qualquer coisa tem o arquivo teste pra você ver como funciona.

## Utilização

Faz assim para so rodar main dentro do seu arquivo:
	

    python3 main.py <seu_arquivo>

Assim para rodar o terminal:


    python3 main.py 

E assim pra rodar o terminal e carregar as suas subrotinas definidas dentro do arquivo:


    python3 main.py -l <seu_arquivo>