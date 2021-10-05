from math import sqrt

posiçãoROBO = [1,7]

posiçãoBLOCOS =[['R', 0, 1],
                ['W', 3, 3],
                ['K', 2, 0],
                ['G', 7, 2],
                ['W', 1, 2],
                ['K', 0, 0],
                ['B', 5, 2],
                ['K', 5, 1]]

def melhorbloco(posiçãorobo, arrayvisão):
    posiçãoROBO = posiçãorobo
    posiçãoBLOCOS = arrayvisão
    matriz = [ [3,2],[3,3],[4,2],[4,3],[3,5],[3,6],[4,5],[4,6] ]
    pratileira = [1,4]
    lista_valores_blocos = []
    lista_posiçoes_blocos = []
    def valorBLOCO(l):
        #l elemento que está iterando na lista "posiçãoBLOCOS"
        peso = bloquinho(l[0], l[1], l[2])
        quadrante = l[1]
        elementomatriz = matriz[quadrante] 
        dist = distancia(posiçãorobo, elementomatriz)+ distancia(elementomatriz, pratileira)
        valor = peso//dist
        lista_valores_blocos.append(valor)
        lista_posiçoes_blocos.append([l[1],l[2]])

    def centro(setor, posiçãosetor):
        blocos_no_centro =[[0,3],[1,2],[2,1],[3,0],[4,3],[5,2],[6,1],[7,0]]
        a = [setor, posiçãosetor]
        if a in blocos_no_centro:
            return True
        else:
            return False

    def bloquinho(bloco, setor, posiçãosetor):
        if bloco == 'W':#brancos
            if not centro(setor, posiçãosetor):
                return 10000
            else:
                return 0
        elif bloco =='R':#red
            if not  centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco =='Y':#yellow
            if  not centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco == 'K':#black
            if not centro(setor, posiçãosetor):
                return 500
            else:
                return 0
        elif bloco =='G':#green
            if not centro(setor, posiçãosetor):
                return 100
            else:
                return 0
        elif bloco == '0':#empty
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
        xr =origem[0]
        yr = origem[1]
        xm = destino[0]
        ym = destino[1]
        distance = sqrt( (xr-xm)**2 + (yr-ym)**2)
        return distance

    for b in arrayvisão:
        valorBLOCO(b)

    maior= lista_valores_blocos.index(max(lista_valores_blocos))
    posiçãoBLOCOS[maior][0] = 0
    bloco_escolhido =lista_posiçoes_blocos[maior]
    return bloco_escolhido


def trajeto(bloco):
    matriz = [[3,2],[3,3],[4,2],[4,3],[3,5],[3,6],[4,5],[4,6]]
    setor = bloco[0]
    superiores = [[32],[33],[35],[36]]
    inferiores = [[42],[43],[45],[46]]
    diminuir = [[32],[42], [35],[45]]
    aumentar = [[33],[43], [36],[46]]  
    blocofinal = ''
    for l in bloco:
         l = str(l)
         blocofinal+=l
    blocofinal = int(blocofinal)
    if blocofinal in inferiores:
        if blocofinal[1] == 2 or blocofinal[1] == 3:
            return blocofinal+10
    elif blocofinal in superiores:
        if blocofinal[1] ==2 or blocofinal[1]==3:
            return blocofinal-10
    elif blocofinal in diminuir:
        if blocofinal[1] ==0 or blocofinal[1] ==2:
            return blocofinal-1
    elif blocofinal in aumentar:
        if blocofinal[1] == 1 or blocofinal[1]==3:
            return blocofinal+1
    
