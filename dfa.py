fin = open("dfa.in", "r")
fout = open("output.out", "w")

def get_section_list():
    l = []
    d = {}
    for linie in fin:
        linie = linie.replace(",", " ")
        l = linie.split()
        if l:
            if l[0][0] != '#':
                if l[0][0] == '[' and l[0][-1] == ']':
                    if l[0] in d.keys():
                        raise Exception("Sectiunea a mai fost o data definita!")
                    else:
                        d[l[0]] = []
                        cheie = l[0]
                else:
                    if cheie == "[Sigma]":
                        if l[0] not in d[cheie]:
                            d[cheie].append(l[0])
                    else:
                        ok1 = 0
                        for x in d[cheie]:
                            ok2 = 0
                            if len(x) == len(l):
                                for j in range(len(x)):
                                    if l[j] == x[j]:
                                        ok2 = ok2 + 1
                            if ok2 == len(x):
                                ok1 = 1
                        if ok1 == 0:
                            d[cheie].append(l)
    return d

def get_sigma(d):
    cheie = "[Sigma]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul nu a fost precizat!")
    return d[cheie]

def get_states(d):
    stari = []
    start = []
    finale = []
    cheie = "[States]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Starile nu au fost precizate!")
    for x in d[cheie]:
        stari.append(x[0])
        if 'S' in x:
            start.append(x[0])
        if 'F' in x:
            finale.append(x[0])
    if len(start) == 0:
        raise Exception("Starea initiala nu a fost precizata!")
    if len(start) > 1:
        raise Exception("Au fost precizate mai multe stari initiale!")
    if len(finale) == 0:
        raise Exception("Nu a fost precizata nicio stare finala!")
    return stari, start, finale

def get_delta(d):
    cheie = "[Delta]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Functia delta nu a fost precizata!")
    for x in d[cheie]:
        if x[0] not in stari:
            raise Exception(f"Starea {x[0]} nu este definita!")
        if x[1] not in d["[Sigma]"]:
            raise Exception(f"Litera {x[1]} nu face parte din alfabetul definit!")
        if x[2] not in stari:
            raise Exception(f"Starea {x[0]} nu este definita!")
    for i in range(len(d[cheie])):
        for j in range(i + 1, len(d[cheie])):
            if d[cheie][i][0] == d[cheie][j][0] and d[cheie][i][1] == d[cheie][j][1] and d[cheie][i][2] != d[cheie][j][2]:
                raise Exception(f"Functia Delta nu a fost bine definita! "
                                f"Vezi ce se intampla cand automatul primeste {d[cheie][i][1]}")
    return d[cheie]

def emulate_dfa(stari, alfabet, start, finale, delta, s1):
    q = start[0]
    for s in s1:
        ok = 0
        for x in delta:
            if x[0] == q and x[1] == s:
                q = x[2]
                ok = 1
                break
        if ok == 0:
            return 0
    if q in finale:
        return 1
    return 0

def afisare(stari, alfabet, start, finale, delta):
    fout.write("[States]\n")
    for x in stari:
        fout.write(x)
        fout.write("\n")
    fout.write("\n[Sigma]\n")
    for x in alfabet:
        fout.write(x)
        fout.write("\n")
    fout.write("\n[Initial State]\n")
    fout.write(start[0])
    fout.write("\n")
    fout.write("\n[Final States]\n")
    for x in finale:
        fout.write(x)
        fout.write("\n")
    fout.write("\n[Delta]\n")
    for x in delta:
        for y in x:
            fout.write(y)
            fout.write(" ")
        fout.write("\n")

d = get_section_list()
alfabet = get_sigma(d)
stari, start, finale = get_states(d)
delta = get_delta(d)
print("Configuratia automatului este OK!")
afisare(stari, alfabet, start, finale, delta)

s1 = input("Introduceti limbajul dorit: ")
rezultat = emulate_dfa(stari, alfabet, start, finale, delta, s1)
if rezultat == 1:
    print("Automatul recunoaste limbajul introdus!")
else:
    print("Automatul nu recunoaste limbajul introdus!")
