import numpy as np
import math
import random
import time

m = 50000  # iterações
p = 44  # número de possibilidades do CNP para cada instrumento
# não estou usando p no momento, porque os resultados são contínuos
HMS = 5  # numero de harmonias na HM
ni = 30  # numero de instrumentos (cada instrumento seria uma dimensão da função)

HMCR = 0.9
PAR = 0.3
Discreta = False
mpap = 0.45  # O range a ser utilizado no ajuste de nota (escolher um vizinho do CNP) quando a variável é continua
mpai = 3  # O range a ser utilizado no ajuste de nota (escolher um vizinho do CNP) quando a variável é discreta;

media = 0  # resultado médio
mediai = 0  # média de iterações
vezes = 50


# Sphere function
def qualidade(x):
   suma = 0
   for i in range(0, ni):  # para cada dimensão
       suma = suma + (x[i] ** 2)

   return -suma
#
#
# # Rosenbrock function
# def qualidade(x):
#    sum = 0
#
#    for i in range(0, ni - 1):
#        xi = x[i]
#        xnext = x[i + 1]
#        sum = sum + (100 * (xnext - xi ** 2) ** 2 + (xi - 1) ** 2)
#
#    return -sum  # quanto maior o somatório, menor será a qualidade da harmonia, porque eu quero o minimo global
#
#
# # Ackley
# def qualidade(x):
#     sum01 = 0
#     sum02 = 0
#
#     for i in range(0, ni):  # para cada dimensão
#         sum01 = sum01 + (x[i] ** 2)
#         sum02 = sum02 + math.cos(2 * math.pi)
#
#     term01 = -20 * math.exp(-0.2 * (sum01 / ni) ** (1 / 2))
#     term02 = -1 * math.exp(sum02 / ni)
#
#     return -round((term01 + term02 + 20 + math.exp(1)), 5)
#
#
# # Griewank
# def qualidade(x):
#      sum01 = 0
#      produ = 1
#      for i in range(0, ni):
#          sum01 = sum01 + (x[i] ** 2 / 4000)
#          produ = produ * math.cos(x[i] / ((i + 1) ** (1 / 2)))
#
#      return -(sum01 - produ + 1)


def considerarhm(j):
    aleatorio = random.randint(0, HMS - 1)
    auxi = list(HM.values())
    return auxi[aleatorio][j]


def considerarcnp(j, z):
    if Discreta:
        return random.choice(cnp[j])  # Dentre as p possibilidades para os ni instrumentos, escolhe-se um aleatoriamente
    else:
        return round(random.uniform(inf + z, sup + z), 5)


def ajustarnota(aux, j, z):
    if not Discreta:
        if random.random() < 0.5:
            return aux - ((aux - (inf + z)) * random.uniform(0, mpap))
        else:
            return aux + (((sup + z) - aux) * random.uniform(0, mpap))
    else:
        posicao = np.where(cnp[j] == aux)[0]
        if random.random() < 0.5:  # Será escolhido um dos vizinhos inferiores
            if mpai < posicao:
                return cnp[j][posicao - random.randint(0, mpai)]
            else:
                return cnp[j][posicao - random.randint(0, posicao)]
        else:  # Será escolhido um dos vizinhos superiores
            if mpai < ((len(cnp[j]) - posicao) - 1):
                return cnp[j][posicao + random.randint(0, mpai)]
            else:
                return cnp[j][posicao + random.randint(0, len(cnp[j]) - posicao - 1)]


def atualizarmemoria(y):
    newQuality = round(qualidade(y), 5)
    menor = sorted(list(HM.keys()))[0]
    if newQuality not in HM:
        if newQuality > menor:
            del HM[menor]
            HM[newQuality] = y


# Definir o Conjunto de Notas Possíveis (CNP) inicial para cada instrumento
def definircnp():
    for ii in range(0, ni):
        for jj in range(0, p):
            cnp[ii][jj] = random.uniform(inf, sup)


melatual = np.empty([vezes])  # mel é melhor, no mel atual cada dimensão guarda o melhor resultado daquela iteração
iatual = np.zeros([vezes])
start_time = time.time()
mel = 1000000
for execu in range(vezes):  # quantas execuções
    inf = -100
    sup = 100
    HM = {}
    if Discreta:
        cnp = np.empty([ni, p])
        definircnp()

    # Preenche a HM inicial com valores aleatórios baseados no CNP
    aux = np.empty([HMS, ni])
    z = 0
    for i in range(0, HMS):
        for j in range(0, ni):
            aux[i][j] = considerarcnp(j, z)
        HM[qualidade(aux[i])] = aux[i]

    for i in range(0, m):  # quantas iterações por execução
        novaHarmonia = np.empty([ni])
        # Redefinir os limites, baseado no pior da HM
        if i % 1000 == 0:
            inf = (-1 * abs(min(list(HM[max(list(HM.keys()))]))))
            sup = abs(max(list(HM[max(list(HM.keys()))])))
            if random.random() < 0.5:
                z = 1
            else:
                z = -1

            sup = sup + z
            inf = inf + z

        if random.random() < 0.5:
            z = 1
        else:
            z = -1
        for j in range(0, ni):
            if random.random() < HMCR:
                novaHarmonia[j] = round(considerarhm(j), 5)
                if random.random() < PAR:
                    novaHarmonia[j] = round(ajustarnota(novaHarmonia[j], j, z), 5)
            else:
                novaHarmonia[j] = round(considerarcnp(j, z), 5)
        atualizarmemoria(novaHarmonia)

        if sorted(list(HM.keys()))[len(HM.keys()) - 1] == 0:  # Se encontrou a melhor solução
            print("\nvalor de i atual: ", i + 1)
            mediai = mediai + 1
            iatual[execu] = i + 1
            break
        mediai = mediai + 1

    melatual[execu] = -1 * max(list(HM.keys()))  # pega o melhor resultado dessa iteração
    print(f"melhor solução da {execu + 1}º execução: {melatual[execu]}")
    print(f"melhor solução da {execu + 1}º execução: {HM[-melatual[execu]]}")
    print("--- %s seconds ---" % (time.time() - start_time))

    media = media + melatual[execu]
    if melatual[execu] < mel:
        mel = melatual[execu]

print(f"\n\n--- tempo médio: {(time.time() - start_time) / vezes} seconds")

media = media / vezes
mediai = mediai / vezes

variancia = 0
variancia02 = 0
desvioabsolutomedio = 0
desvioabsolutomedio02 = 0
for execu in range(vezes):
    if iatual[execu] == 0:
        iatual[execu] = m

for execu in range(vezes):
    variancia02 = variancia02 + (iatual[execu] - mediai) ** 2
    variancia = variancia + (melatual[execu] - media) ** 2
    desvioabsolutomedio = desvioabsolutomedio + abs(melatual[execu] - media)
    desvioabsolutomedio02 = desvioabsolutomedio02 + abs(iatual[execu] - mediai)

desvio = (variancia / vezes) ** (1 / 2)
desvio02 = (variancia02 / vezes) ** (1 / 2)  # desvio de quantidade de iterações
desvioabsolutomedio = desvioabsolutomedio / vezes
desvioabsolutomedio02 = desvioabsolutomedio02 / vezes  # regarding iterações

print(f"\nmédia iterações: {mediai}")
print(f"Desvio Padrão da quantidade de iterações: {desvio02}")
print(f"Desvio absoluto médio da quantidade de iterações: {desvioabsolutomedio02}")

print(f"\nmelhor de todas execuções: {mel}")
print(f"média: {media}")
print(f"Desvio Padrão dos resultados: {desvio}")
print(f"Desvio absoluto médio dos resultados: {desvioabsolutomedio}")
