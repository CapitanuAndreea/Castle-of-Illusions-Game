#student: Capitanu Andreea
#grupa: 143
fin = open("la.in", "r")

def get_section_list():
    l = []
    d = {}
    #citim cate o linie din fisierul de intrare
    for linie in fin:
        linie = linie.replace(",", " ")
        linie = linie.replace("->", " ")
        linie = linie.replace("(", " ")
        linie = linie.replace(")", " ")
        l = linie.split()
        if l:
            #luam in considerare doar liniile necomentate
            if l[0][0] != '#':
                #parantezarea patrata reprezinta inceputul unei noi sectiuni
                if l[0][0] == '[' and l[0][-1] == ']':
                    if l[0] in d.keys():
                        raise Exception("Sectiunea a mai fost o data definita!")
                    else:
                        #adaugam in dictionarul d o cheie cu numele sectiunii
                        d[l[0]] = []
                        cheie = l[0]
                else:
                    #adaugam elementele in dictionar, la cheia potrivita
                    if cheie == "[Sigma]" or cheie == "[Gamma]":
                        d[cheie].append(l[0])
                    else:
                        d[cheie].append(l)
    return d

#functia are rolul de a sesiza posibilele erori
#si de a retine alfabetul intr-un set(pentru a nu aparea aceeasi stare de mai multe ori)
def get_sigma(d):
    cheie = "[Sigma]"
    d[cheie] = set(d[cheie])
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul nu a fost precizat!")
    return d[cheie]

#functia are rolul de a sesiza posibilele erori
#si de a retine alfabetul listei intr-un set
def get_gamma(d):
    cheie = "[Gamma]"
    d[cheie] = set(d[cheie])
    #cu e vom nota epsilon
    d[cheie].add('e')
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul listei nu a fost precizat!")
    return d[cheie]

#retinem in stari-multimea starilor
#in start-starea de inceput
#in finale-starile finale
def get_states(d):
    stari = []
    start = []
    finale = []
    cheie = "[States]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Starile nu au fost precizate!")
    for x in d[cheie]:
        stari.append(x[0])
        #daca starea este urmata de S inseamna ca este starea initiala
        if 'S' in x:
            start.append(x[0])
        #daca starea este urmata de F, o adaugam si in multimea starilor finale
        if 'F' in x:
            finale.append(x[0])
    #tratam posibilele erori
    if len(start) == 0:
        raise Exception("Starea initiala nu a fost precizata!")
    if len(start) > 1:
        raise Exception("Au fost precizate mai multe stari initiale!")
    if len(finale) == 0:
        raise Exception("Nu a fost precizata nicio stare finala!")
    return stari, start, finale

#functia are rolul de a sesiza posibilele erori la definirea functiei de tranzitie
#s de a retine definitia ei intr-o lista de liste
def get_delta(d):
    cheie = "[Delta]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Functia delta nu a fost precizata!")
    for x in d[cheie]:
        if x[0] not in stari:
            raise Exception(f"Starea {x[0]} nu este definita!")
        if x[1] not in d["[Sigma]"]:
            raise Exception(f"Litera {x[1]} nu face parte din alfabetul definit!")
        if x[2] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[2]} nu face parte din alfabetul definit pentru lista!")
        if x[3] not in stari:
            raise Exception(f"Starea {x[3]} nu este definita!")
        if x[4] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[4]} nu face parte din alfabetul definit pentru lista!")
        if x[5] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[5]} nu face parte din alfabetul definit pentru lista!")
    return d[cheie]

#functie care verifica daca elementul b se afla in lista automatului
def check(b, lista):
    if b in lista:
        return 1
    return 0

#functie care testeaza daca automatul accepta limbajul s1, citit din stdin
#automatul accepta limbajul s1 daca la finalul parcurgerii inputului,
#automatul se afla intr-o stare finala
def emulate_la(stari, alfabet, gamma, start, finale, delta, s1, s, stare_init, lista):
    #cu indicele s se parcurge sirul s1
    if s == len(s1):
        #variabila stare_init se refera la starea in care se afla automatul la pasul curent
        #daca s-a terminat de parcurs inputul si starea curenta a automatului nu este una final
        #returnam false
        if stare_init not in finale:
            return 0
        #altfel, afisam rezultatul pozitiv si incheiem recursia
        print("Automatul recunoaste limbajul introdus!")
        exit(0)
    for x in delta:
        #un element din delta arata asa:
        #(q1, a, b) -> (q2, a2, a3)
        #parcurgem functia de tranzitie si cautam un element cu
        #q1-starea noastra curenta si a-litera curenta
        if x[0] == stare_init:
            if x[1] == s1[s]:
                #crestem indicele s
                s = s + 1
                if x[2] != 'e':
                    #verificam daca b este in lista automatului
                    check(x[2], lista)
                if x[4] != 'e':
                    #daca a2 != e este in lista, il eliminam
                    if x[4] in lista:
                        lista.remove(x[4])
                if x[5] != 'e':
                    #daca a3 != e, il adaugam in lista
                    lista.add(x[5])
                #apelam functia pentru urmatoarea litera din s1
                #si pentru noua stare curenta-q2
                emulate_la(stari, alfabet, gamma, start, finale, delta, s1, s, x[3], lista)

#ne declaram structurile de care avem nevoie
d = get_section_list()
alfabet = get_sigma(d)
gamma = get_gamma(d)
stari, start, finale = get_states(d)
delta = get_delta(d)
lista = set()

#se afiseaza daca programul nu a aruncat nicio eroare
print("Configuratia automatului este OK!")

#citim de la stdin limbajul pe care dorim sa il verificam
s1 = input("Introduceti limbajul dorit: ")

#apelam functia care ne verifica limbajul ales
raspuns = emulate_la(stari, alfabet, gamma, start, finale, delta, s1, 0, start[0], lista)

#daca programul nu s-a incheiat deja
#inseamna ca automatul nu recunoaste limbajul ales
if raspuns != 1:
    print("Automatul nu recunoaste limbajul introdus!")