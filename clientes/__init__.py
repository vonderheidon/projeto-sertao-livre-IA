from layouts import *
from bd import *
import matplotlib.pyplot as plt
import torch
from torchvision import models, transforms
from PIL import Image
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def menuCliente(texto):
    while True:
        menu = layMsec(texto)
        if (menu == '1'):
            cadastrarUsuario('cliente')
        elif (menu == '2'):
            cid = entrar('cliente')
            if (cid != None):
                menuPrincipal(cid)
                break
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def menuPrincipal(cid):
    while True:
        texto = ('\n[1] - Meu perfil\n[2] - Minhas Compras\n[3] - Pesquisar produtos\n[4] - Meu Carrinho\n[0] - Sair da conta')
        menu = layMPrincipal(clientes, cid, texto)
        if (menu == '1'):
            meuPerfil(cid)
        elif (menu == '2'):
            minhasCompras(cid)
        elif (menu == '3'):
            pesquisarProd(cid)
        elif (menu == '4'):
            meuCarrinho(cid)
        elif (menu == '0'):
            carrinho.clear()
            iniCar[0] = 0
            break
        else:
            erro('Opcao invalida.')

def meuPerfil(cid):
    while True:
        menu = layMmperf(clientes, cid)
        if (menu == '1'):
            atualizarInfoPessoais(cid)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

def atualizarInfoPessoais(cid):
    while True:
        menu = layAttinf(clientes, cid)
        if (menu == '1'):
            atualizarDados(clientes, cid, 'O seu nome completo', 3, 2)
        elif (menu == '2'):
            atualizarDados(clientes, cid, 'O seu email', 3, 3)
        elif (menu == '3'):
            atualizarUsuario(clientes, cid, 'O seu usuario', 3)
        elif (menu == '4'):
            atualizarSenha(clientes, cid, 'A sua senha', 6)
        elif (menu == '0'):
            break
        else:
            erro('Opcao invalida.')

##################################################################################################################################################################################

def minhasCompras(cid):
    if existeItem(compras, cid):
        while True:
            print(f'\n{CBLU}'+ (50 * '-'))
            print(f'     Lista de pedidos | {clientes[cid][2]}')
            print((50 * '-')+ f'{CEND}')
            pedidos = retornaPedidos(cid)
            for chave in pedidos.keys():
                print(f'\nCod: {CGRE}{chave}{CEND}')
                for item in pedidos[chave]:
                    print(f'{item[1]} - Un: {item[4]}')
            print('\n[1] - Exibir detalhes\n[0] - Voltar ao menu anterior')
            opcao = str(input('\nDigite a opcao desejada: '))
            if (opcao == '1'):
                cod = str(input('Digite o código do pedido: '))
                if cod in pedidos.keys():
                    detalhaPedidos(cod,pedidos)
                    input('\nPressione ENTER para voltar o menu anterior.')
                else:
                    erro('Pedido não encontrado.')
            elif (opcao == '0'):
                break
            else:
                erro('Opção inválida.')
    else:
        erro('Você ainda não fez nenhuma compra.')
        return

def meuCarrinho(cid):
    removido = False
    while True:
        if (len(carrinho) > 0):
            print(f'\n{CBLU}'+ (50 * '-'))
            print(f'    Meu carrinho | {clientes[cid][2]}')
            print((50 * '-') + f'{CEND}')
            totalPedido = 0
            for chave in carrinho.keys():
                print(f'\nItem nº {CGRE}{chave}{CEND} | cod: {carrinho[chave][0]} - {carrinho[chave][1]} - Descrição: {carrinho[chave][3]}\nQuantidade: {carrinho[chave][4]} - Preço un. R$ {carrinho[chave][2]:.2f}')
                total = carrinho[chave][2] * carrinho[chave][4]
                totalPedido += total
                print(f'Total: R$ {total:.2f}')
            print(f'\nTotal do pedido: R$ {totalPedido:.2f}')
            print('\n[1] - Remover item do carrinho\n[2] - Finalizar compra\n[0] - Voltar ao menu anterior')
            opcao = str(input('\nDigite a opcao desejada: '))
            if (opcao == '1'):
                item = verInputNum('Digite numero do item: ',tipo='int')
                if (item != 'erro'):
                    if item in carrinho.keys():
                        qtd = carrinho[item][4]
                        cod = carrinho[item][0]
                        vid = selecionaID(cod)
                        manipulaEstoque(vid, cod, qtd, None, op='devolve')
                        carrinho.pop(item)
                        aviso('Item removido do carrinho com sucesso.')
                        removido = True
                    else:
                        erro('Item não encontrado.')
            elif (opcao == '2'):
                finalizaPedido(cid,unico='nao')
                removido = True
            elif (opcao == '0'):
                break
            else:
                erro('Opção inválida.')
        else:
            if removido:
                iniCar[0] = 0
            else:
                aviso('Seu carrinho está vazio ainda.')
            break

def pesquisarProd(cid):
    while True:
        print(f'\n{CBLU}'+ (50 * '-'))
        print(f'  Tela de pesquisa de produtos | {clientes[cid][2]}')
        print((50 * '-') + f'{CEND}')
        print(f'\nPelo o que você deseja pesquisar?')
        print('\n[1] - Nome\n[2] - Descrição\n[3] - Por imagem\n[4] - Ver gráfico dos 5 itens mais pesquisados\n[0] - Voltar ao menu anterior')
        opcao = str(input('\nDigite a opcao desejada: '))
        if (opcao == '1'):
            resultPesquisaProd(1, 'no nome', cid)
        elif (opcao == '2'):
            resultPesquisaProd(3, 'na descrição', cid)
        elif (opcao == '3'):
            produto = reconhecerObjetoImagem()
            if produto:
                resultPesquisaProd(3, 'na descrição', cid, IA=produto)
        elif (opcao == '4'):
            verMaisPesquisados()
        elif (opcao == '0'):
            break
        else:
            erro('Opcao invalida.')

def resultPesquisaProd(campo, prompt, cid, IA=''):
    codigos = dict()
    if (IA != ''):
        busca = IA
    else:
        busca = str(input(f'\nPesquisando {prompt}: ').lower())
    retorna = False
    if (busca != ''):
        while True:
            achei = False
            for prod in produtos.values():
                for item in prod:
                    lowprod = item[campo].lower()
                    if (lowprod.find(busca) >= 0):
                        if not achei:
                            print(f'\n{CYEL}O que encontramos com o termo "{busca}" {prompt}:{CEND}')
                            print(f'\nCódigo -  Produto          -  Preço un.  -  Descrição')
                        print(f'{CGRE} {item[0]}{CEND}  -  {item[1]:<16} -  R$ {item[2]:<7.2f} -  {item[3]}')
                        codigos[item[0]] = item[1]
                        achei = True
            if achei:
                if not retorna:
                    for item in codigos:
                        adicionaPesquisados(item,codigos[item])
                print('\n[1] - Exibir detalhes\n[0] - Voltar ao menu anterior')
                opcao = str(input('\nDigite a opcao desejada: '))
                if (opcao == '1'):
                    cod = str(input('Digite o código do produto: '))
                    if cod in codigos:
                        vid = selecionaID(cod)
                        status = exibirDetalhes(cid, cod, vid)
                        if (status == 'pesquisaOff'):
                            retorna = True
                    else:
                        erro('Produto não encontrado.')
                        retorna = True
                elif (opcao == '0'):
                    break
                else:
                    erro('Opção inválida.')
                    retorna = True
            else:
                erro(f'Nao tem nenhum produto com o termo "{busca}" {prompt}.')
                return
    else:
        erro(f'O campo de pesquisa não deve ficar em branco.')

def verMaisPesquisados():
    cont = 0
    ordenado = []
    #essa parte é toda by google
    ordenado = (sorted(maisPesquisados, key=lambda item: item['qtd'], reverse=True))
    for item in ordenado:
        plt.rcParams["figure.figsize"] = (12, 6)
        plt.bar(f'Cod: {item["cod"]}\nProduto: {item["nome"]}',item['qtd'])
        cont += 1
        if (cont==5):
            break
    plt.show()

def adicionaPesquisados(codProd,nome):
    if (len(maisPesquisados) > 0):
        existe = False
        for itemArm in maisPesquisados:
            if (itemArm['cod'] == codProd):
                itemArm['qtd'] += 1
                existe = True
                break
        if not existe:
            maisPesquisados.append({'cod': codProd, 'nome': nome, 'qtd': 1})
    else:
        maisPesquisados.append({'cod':codProd, 'nome':nome, 'qtd':1})

def exibirDetalhes(cid, cod, vid):
    while True:
        print(f'\n{CBLU}'+ (50 * '-'))
        print(f'    Tela de detalhes do produto | {clientes[cid][2]}')
        print((50 * '-') + f'{CEND}')
        if detalheProduto(vid, cod, compra='sim'):
            print('\n[1] - Comprar\n[2] - Adicionar ao carrinho\n[0] - Voltar ao menu anterior')
            opcao = str(input('\nDigite a opcao desejada: '))
            if (opcao == '1'):
                comprarProduto(cid, cod, vid)
            elif (opcao == '2'):
                adicionaCarrinho(cid, cod, vid)
            elif (opcao == '0'):
                return 'pesquisaOff'
            else:
                erro('Opcao invalida.')
        else:
            erro('Esse produto está esgotado.')
            break

def comprarProduto(cid, cod, vid):
    while True:
        qtd = verInputNum('Digite a quantidade desejada: ',tipo='int')
        if (qtd != 'erro'):
            acao = manipulaEstoque(vid, cod, qtd, unico='sim', op='retira')
            if (acao == 'retirado'):
                finalizaPedido(cid, unico='sim')
                return
            elif (acao == 'insuficiente'):
                erro('A quantidade em estoque é insuficiente para a quantidade informada.')
                break
        else:
            break

def adicionaCarrinho(cid, cod, vid):
    while True:
        qtd = verInputNum('Digite a quantidade desejada: ', tipo='int')
        if (qtd != 'erro'):
            acao = manipulaEstoque(vid, cod, qtd, unico='nao', op='retira')
            if (acao == 'retirado'):
                aviso('Produto adicionado ao carrinho com sucesso.')
                return
            elif (acao == 'insuficiente'):
                erro('A quantidade em estoque é insuficiente para a quantidade informada.')
                break
        else:
            break


def finalizaPedido(cid, unico):
    nid = novoIdCompra(cid)
    for chave1 in compras:
        if (chave1 == cid):
            compras[chave1].append({nid: []})
            for dicicionario1 in compras[chave1]:
                for chave2 in dicicionario1:
                    if (chave2 == nid):
                        if (unico == 'sim'):
                            dicicionario1[chave2].append(cartemp[0])
                            cartemp.clear()
                        elif (unico == 'nao'):
                            for pedido in carrinho.values():
                                dicicionario1[chave2].append(pedido)
                            carrinho.clear()
                            iniCar[0] = 0
                        break
            break
    aviso(f'Pedido código {nid} finalizado com sucesso.')

def selecionaImagem():
    try:
        app = QApplication(sys.argv)
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Imagens (*.jpg *.jpeg)")
        if dialog.exec_():
            caminho_imagem = dialog.selectedFiles()[0]
            return caminho_imagem
        return None
    except:
        return None

def traduzObjeto(nomeObjeto):
    try:
        if nomeObjeto:
            if nomeObjeto == '"banana",':
                return 'Banana'
            elif nomeObjeto == '"orange",':
                return 'Laranja'
            elif nomeObjeto == '"strawberry",':
                return 'Morango'
            elif nomeObjeto == '"pineapple",':
                return 'Abacaxi'
            elif nomeObjeto == '"meatloaf",':
                return 'Carne'
            elif nomeObjeto == '"desktop computer",':
                return 'Computador'
            elif nomeObjeto == '"notebook computer",':
                return 'Notebook'
            elif nomeObjeto == '"electric fan",':
                return 'Ventilador'
            elif nomeObjeto == '"mobile phone",':
                return 'Celular'
            else:
                print(f'\n{CRED}Esse objeto não foi traduzido, o nome retornado é esse: {nomeObjeto}{CEND}')
                return nomeObjeto
        else:
            return None
    except:
        return None

def reconhecerObjetoImagem():
    try:
        caminhoImagem = selecionaImagem()
        if caminhoImagem:
            modelo = models.resnet50(weights='ResNet50_Weights.DEFAULT')
            modelo.eval()
            transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            imagem = Image.open(caminhoImagem)
            imagem = transform(imagem)
            imagem = imagem.unsqueeze(0)
            with torch.no_grad():
                saida = modelo(imagem)
            with open("classes.txt", "r") as f:
                classes = [linha.strip() for linha in f.readlines()]
            pontuacao, indice = torch.max(saida, 1)
            nomeObjeto = classes[indice.item()]
            traduzido = traduzObjeto(nomeObjeto)
            return traduzido.lower()
        else:
            return None
    except:
        erro('Ocorreu algum erro no sistema de pesquisa por imagem.')
        return None