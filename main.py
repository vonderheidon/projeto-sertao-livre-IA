from layouts import *
from vendedores import *
from clientes import *

while True:
    menu = layMini()
    if (menu == '1'):
        menuVendedor('-------------------------'
                     '\n      Menu vendedor'
                     '\n-------------------------')
    elif (menu == '2'):
        menuCliente('-------------------------'
                    '\n      Menu Cliente'
                    '\n-------------------------')
    elif (menu == '0'):
        break
    else:
        erro('Opcao invalida.')