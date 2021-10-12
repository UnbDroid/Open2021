from math import sqrt

# posiçãoROBO = [1, 7]

# posiçãoBLOCOS = [
#                 ['K' '0' '1']
#                 ['R' '0' '0']
#                 ['W' '1' '3']
#                 ['G' '1' '2']
#                 ['W' '3' '1']
#                 ['K' '3' '2']
#                 ['W' '5' '0']
#                 ['W' '4' '1']
#                 ['K' '4' '3']
#                 ['K' '6' '0']
#                 ['W' '7' '3']
#                 ['B' '7' '2']
#                 ['Y' '6' '3']
#                 ]


def melhorbloco(posicaoRobo, arrayVisao):
    # posicaoRobo = posicaoRobo
    posiçãoBLOCOS = arrayVisao
    matriz = [[3, 2], [3, 3], [4, 2], [4, 3], [3, 5], [3, 6], [4, 5], [4, 6]]
    pratileira = [1, 4]
    lista_valores_blocos = []
    lista_posiçoes_blocos = []

    def valorBLOCO(l):
        # l elemento que está iterando na lista "posiçãoBLOCOS"
        peso = bloquinho(l[0], int(l[1]), int(l[2]))
        quadrante = int(l[1])
        
        elementomatriz = matriz[quadrante]
        print('POSICAO=',posicaoRobo)
        print('ELEMENTO=', elementomatriz)
        print('PRATILEIRA=', pratileira)

        dist = distancia(posicaoRobo, elementomatriz) + distancia(elementomatriz, pratileira)
        valor = peso//dist
        lista_valores_blocos.append(valor)
        lista_posiçoes_blocos.append([l[0],int(l[1]), int(l[2])])

    def centro(setor, posiçãosetor):
        blocos_no_centro = [[0, 3], [1, 2], [2, 1],
                            [3, 0], [4, 3], [5, 2], [6, 1], [7, 0]]
        a = [setor, posiçãosetor]
        if a in blocos_no_centro:
            return True
        else:
            return False

    def bloquinho(bloco, setor, posiçãosetor):
        if bloco == 'W':  # brancos
            if not centro(setor, posiçãosetor):
                return 10000
            else:
                return 0
        elif bloco == 'R':  # red
            if not centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco == 'Y':  # yellow
            if not centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco == 'K':  # black
            if not centro(setor, posiçãosetor):
                return 500
            else:
                return 0
        elif bloco == 'G':  # green
            if not centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco == '0':  # empty
            if not centro(setor, posiçãosetor):
                return 1
            else:
                return 0
        elif bloco == 'B':
            if not centro(setor, posiçãosetor):
                return 100
            else:
                return 0

    def distancia(origem, destino):
        xr = int(origem[0])
        yr = int(origem[1])
        xm = int(destino[0])
        ym = int(destino[1])
        distance = sqrt((xr-xm)**2 + (yr-ym)**2)
        return distance

    for b in arrayVisao:
        valorBLOCO(b)

    maior = lista_valores_blocos.index(max(lista_valores_blocos))
    posiçãoBLOCOS[maior][0] = 0
    bloco_escolhido = lista_posiçoes_blocos[maior]
    return bloco_escolhido


def trajeto(bloco):
    matriz = [32, 33, 42, 43, 35, 36, 45, 46]
    setor = bloco[0]
    superiores = [32, 33, 35, 36]
    inferiores = [42, 43, 45, 46]
    diminuir = [32, 42, 35, 45]
    aumentar = [33, 43, 36, 46]
    teste = bloco
    # aumentar = [3, 1, 5, 7]
    blocofinal = matriz[bloco[1]]
    # for l in bloco:
    #     l = str(l)
    #     blocofinal += l
    # blocofinal = int(blocofinal)
    print('******',blocofinal)
    if blocofinal in inferiores:
        if bloco[2] == 2 or bloco[2] == 3:
            return blocofinal+10
    if blocofinal in superiores:
        if bloco[2] == 0 or bloco[2] == 1:
            return blocofinal-10
    if blocofinal in diminuir:
        if bloco[2] == 0 or bloco[2] == 2:
            return blocofinal-1
    if blocofinal in aumentar:
        if bloco[2] == 1 or bloco[2] == 3:
            return blocofinal+1
    else:
        print("DEU RUIM")


def invertMatrix(matrix):

    for block in matrix:
        if(block[1] == '0'):
            block[1] = '3'
        elif(block[1] == '1'):
            block[1] = '2'
        elif(block[1] == '2'):
            block[1] = '1'
        elif(block[1] == '3'):
            block[1] = '0'
        elif(block[1] == '4'):
            block[1] = '7'
        elif(block[1] == '5'):
            block[1] = '6'
        elif(block[1] == '6'):
            block[1] = '5'
        elif(block[1] == '7'):
            block[1] = '4'

        if(block[2] == '0'):
            block[2] = '3'
        elif(block[2] == '1'):
            block[2] = '2'
        elif(block[2] == '2'):
            block[2] = '1'
        elif(block[2] == '3'):
            block[2] = '0'
    return matrix

# melhorbloco(posicaoRobo,posiçãoBLOCOS)