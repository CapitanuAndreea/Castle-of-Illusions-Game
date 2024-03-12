fin = open("pda.in", "r")

def get_section_list():
    l = []
    d = {}
    for linie in fin:
        linie = linie.replace(",", " ")
        linie = linie.replace("->", " ")
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
                    if cheie == "[Sigma]" or cheie == "[Gamma]":
                        d[cheie].append(l[0])
                    else:
                        d[cheie].append(l)
    return d

def get_sigma(d):
    cheie = "[Sigma]"
    d[cheie] = set(d[cheie])
    d[cheie].add('e')
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul nu a fost precizat!")
    return d[cheie]

def get_gamma(d):
    cheie = "[Gamma]"
    d[cheie] = set(d[cheie])
    d[cheie].add('e')
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul stivei nu a fost precizat!")
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
        if x[2] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[2]} nu face parte din alfabetul definit pentru stiva!")
        if x[3] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[3]} nu face parte din alfabetul definit pentru stiva!")
        if x[4] not in stari:
            raise Exception(f"Starea {x[4]} nu este definita!")
    return d[cheie]

def emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, s, stare_init, stack):
    if s == len(s1):
        if len(stack) != 0:
            return 0
        if stare_init not in finale:
            return 0
        print("Automatul recunoaste limbajul introdus!")
        exit(0)
    for x in delta:
        if x[0] == stare_init:
            if x[1] != 'e':
                if x[1] == s1[s]:
                    s = s + 1
                    if x[2] != 'e':
                        if len(stack) > 0:
                            if stack[-1] == x[2]:
                                stack.pop()
                                if x[3] != 'e':
                                    stack.append(x[3])
                                emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, s, x[4], stack)
                    else:
                        if x[3] != 'e':
                            stack.append(x[3])
                        emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, s, x[4], stack)
            else:
                if x[2] != 'e':
                    if len(stack) > 0:
                        if stack[-1] == x[2]:
                            stack.pop()
                            if x[3] != 'e':
                                stack.append(x[3])
                            emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, s, x[4], stack)
                else:
                    if x[3] != 'e':
                        stack.append(x[3])
                    emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, s, x[4], stack)

d = get_section_list()
alfabet = get_sigma(d)
gamma = get_gamma(d)
stari, start, finale = get_states(d)
delta = get_delta(d)
print("Configuratia automatului este OK!")
s1 = input("Introduceti limbajul dorit: ")
stack = []
raspuns = emulate_pda(stari, alfabet, gamma, start, finale, delta, s1, 0, start[0], stack)
if raspuns != 1:
    print("Automatul nu recunoaste limbajul introdus!")