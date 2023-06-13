from layouts import *
from bd import *
import matplotlib.pyplot as plt

def menuVendedor(texto):
    while True:
        menu = layMsec(texto)
        if (menu == '1'):
            cadastrarUsuario('vendedor')
        elif (menu == '2'):
            vid = entrar('vendedor')
            if (vid != None):
                menuPrincipal(vid)
                break
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def menuPrincipal(vid):
    while True:
        texto = ('\n[1] - Meu perfil\n[2] - Meus produtos\n[0] - Sair da conta')
        menu = layMPrincipal(vendedores, vid, texto)
        if (menu == '1'):
            meuPerfil(vid)
        elif (menu == '2'):
            meusProdutos(vid)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def meuPerfil(vid):
    while True:
        menu = layMmperf(vendedores, vid)
        if (menu == '1'):
            atualizarInfoPessoais(vid)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def atualizarInfoPessoais(vid):
    while True:
        menu = layAttinf(vendedores, vid)
        if (menu == '1'):
            atualizarDados(vendedores, vid, 'O seu nome completo', 3, 2)
        elif (menu == '2'):
            atualizarDados(vendedores, vid, 'O seu email', 3, 3)
        elif (menu == '3'):
            atualizarUsuario(vendedores, vid, 'O seu usuario', 3)
        elif (menu == '4'):
            atualizarSenha(vendedores, vid, 'A sua senha', 6)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

##################################################################################################################################################################################

def meusProdutos(vid):
    while True:
        menu = layMmprod(vendedores,vid)
        if (menu == '1'):
            listarProdutos(vid)
        elif (menu == '2'):
            listarComGrafico(vid)
        elif (menu == '3'):
            cadastraProduto(vid)
        elif (menu == '4'):
            pesquisarProduto(vid)
        elif (menu == '5'):
            salvaEmTxt(vid)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def listarProdutos(vid):
    while True:
        if existeItem(produtos, vid):
            codigos = list()
            print(f'\n{CGRE}' + (50 * '-'))
            print(f'    Tela produtos cadastrados | {vendedores[vid][2]}')
            print((50 * '-') + f'{CEND}')
            print(f'\nCódigo - Produto')
            for item in produtos[vid]:
                codigos.append(item[0])
                print(f' {CGRE}{item[0]}{CEND}  - {item[1]}')
            print('\n[1] - Exibir detalhes\n[0] - Voltar ao menu anterior')
            opcao = str(input('\nDigite a opcao desejada: '))
            if (opcao == '1'):
                cod = str(input('Digite o código do produto: '))
                if cod in codigos:
                    exibirDetalhes(vid, cod)
                    if not existeItem(produtos, vid):
                        break
                else:
                    erro('Produto não encontrado.')
            elif (opcao == '0'):
                break
            else:
                erro('Opção inválida.')
        else:
            erro('Você ainda não tem nenhum produto cadastrado.')
            return

def listarComGrafico(vid):
    if existeItem(produtos, vid):
        for item in produtos[vid]:
            plt.rcParams["figure.figsize"] = (12, 6)
            plt.bar(f'Produto: {item[1]}\nQuantidade: {item[4]}', item[4])
        plt.show()
    else:
        erro('Você ainda não tem nenhum produto cadastrado.')

def salvaEmTxt(vid):
    if existeItem(produtos, vid):
        nome = vendedores[vid][0]
        prompt = (f'produtosEmTxt\Produtos_{nome}.txt')
        arquivo =  open(prompt, 'w')
        for prod in produtos[vid]:
            arquivo.write(f'Código: {prod[0]}')
            arquivo.write(f'\nNome: {prod[1]}')
            arquivo.write(f'\nPreço: R$ {prod[2]:.2f}')
            arquivo.write(f'\nDescrição: {prod[3]}')
            arquivo.write(f'\nQuantidade em estoque: {prod[4]}\n\n')
        arquivo.close()
        aviso(f'O arquivo "{prompt}" foi gerado com sucesso.')
    else:
        erro('Você ainda não tem nenhum produto cadastrado.')

def cadastraProduto(vid):
    print(f'\n{CGRE}' + (50 * '-'))
    print(f'    Tela de cadastro de produto | {vendedores[vid][2]}')
    print((50 * '-') + f'{CEND}')
    nome = verInputStr(3, '\nNome: ', 'O nome do produto')
    if (nome != False):
        preco = verInputNum('Preço: R$ ',tipo='float')
        if (preco != 'erro'):
            descricao = verInputStr(3, 'Descrição: ', 'O campo descrição')
            if (descricao != 'erro'):
                quantidade = verInputNum('Quantidade: ',tipo='int')
                if (quantidade != 'erro'):
                    iniProd[vid] += 1
                    idProd = f'{vid}' + f'{iniProd[vid]:03}'
                    produtos[vid].append([idProd, nome, preco, descricao, quantidade])
                    aviso('Produto cadastrado com sucesso.')

def exibirDetalhes(vid, cod):
    while True:
        print(f'\n{CBLU}' + (50 * '-'))
        print(f'    Tela de detalhes do produto | {vendedores[vid][2]}')
        print((50 * '-') + f'{CEND}')
        detalheProduto(vid, cod)
        print('\n[1] - Editar\n[2] - Excluir\n[0] - Voltar ao menu anterior')
        opcao = str(input('\nDigite a opcao desejada: '))
        if (opcao == '1'):
            atualizarProduto(vid, cod)
        elif (opcao == '2'):
            if excluirProduto(vid,cod):
                break
        elif (opcao == '0'):
            break
        else:
            erro('Opcao invalida.')

def atualizarProduto(vid, cod):
    while True:
        print(f'\n{CGRE}' + (50 * '-'))
        print(f'   Tela de atualização do produto | {vendedores[vid][2]}')
        print((50 * '-') + f'{CEND}')
        print('\n[1] - Nome\n[2] - Preço\n[3] - Descrição\n[4] - Quantidade\n[0] - Voltar ao menu anterior')
        opcao = str(input('\nDigite a opcao desejada: '))
        if (opcao == '1'):
            attProd(vid, 'O nome', 3, 1, cod)
        elif (opcao == '2'):
            attProd(vid, 'O preço', None, 2, cod, tipo='float')
        elif (opcao == '3'):
            attProd(vid, 'A descrição', 3, 3, cod)
        elif (opcao == '4'):
            attProd(vid, 'A quantidade', None, 4, cod, tipo='int')
        elif (opcao == '0'):
            break
        else:
            erro('Opcao invalida.')

def excluirProduto(vid, cod):
    confirma = input('\nVoce realmente deseja excluir o produto selecionado? [S/N]: ').upper()
    if (confirma == 'S'):
        excluiProduto(vid, cod)
        aviso('Produto excluido com sucesso.')
        return True
    elif (confirma == 'N'):
        return False
    else:
        erro('Opção inválida.')

def pesquisarProduto(vid):
    while True:
        if existeItem(produtos, vid):
            print(f'\n{CGRE}' + (50 * '-'))
            print(f'    Tela de pesquisa de produtos | {vendedores[vid][2]}')
            print((50 * '-') + f'{CEND}')
            print(f'\nPelo o que você deseja pesquisar?')
            print('\n[1] - Nome\n[2] - Descrição\n[0] - Voltar ao menu anterior')
            opcao = str(input('\nDigite a opcao desejada: '))
            if (opcao == '1'):
                pesquisaProd(vid, 1, 'no nome')
                if not existeItem(produtos, vid):
                    break
            elif (opcao == '2'):
                pesquisaProd(vid, 3, 'na descrição')
                if not existeItem(produtos, vid):
                    break
            elif (opcao == '0'):
                break
            else:
                erro('Opcao invalida.')
        else:
            erro('Você não tem nenhum produto cadastrado ainda.')
            return

def pesquisaProd(vid, campo, prompt):
    codigos = list()
    busca = str(input(f'\nPesquisando {prompt}: ').lower())
    if (busca != ''):
        while True:
            achei = False
            for item in produtos[vid]:
                lowprod = item[campo].lower()
                if (lowprod.find(busca) >= 0):
                    codigos.append(item[0])
                    if not achei:
                        print(f'\n{CYEL}O que encontramos com o termo "{busca}" {prompt}:{CEND}')
                        print(f'\nCódigo -  Produto  -  Preço un. -  Descrição')
                    print(f'{CGRE} {item[0]}{CEND}  -  {item[1]:<8} -  R$ {item[2]:<6.2f} -  {item[3]}')
                    achei = True
            if achei:
                print('\n[1] - Exibir detalhes\n[0] - Voltar ao menu anterior')
                opcao = str(input('\nDigite a opcao desejada: '))
                if (opcao == '1'):
                    cod = str(input('Digite o código do produto: '))
                    if cod in codigos:
                        exibirDetalhes(vid, cod)
                        if not existeItem(produtos, vid):
                            return
                    else:
                        erro('Produto não encontrado.')
                elif (opcao == '0'):
                    break
                else:
                    erro('Opção inválida.')
            else:
                erro(f'Nao tem nenhum produto com o termo "{busca}" {prompt}.')
                return
    else:
        erro(f'O campo de pesquisa não deve ficar em branco.')