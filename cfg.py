#student: Capitanu Andreea
#grupa: 143

import random

fin = open("cfg.in", "r")

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
                    elif l[0][1] == 'R':
                        d[l[0]] = {}
                        cheie = l[0]
                    else:
                        d[l[0]] = []
                        cheie = l[0]
                else:
                    if cheie == "[Rules]":
                        if l[0] in d[cheie].keys():
                            d[cheie][l[0]].append(l[2:])
                        else:
                            d[cheie][l[0]] = []
                            a = 2
                            for b in range(2, len(l)):
                                if l[b] == "|":
                                    d[cheie][l[0]].append(l[a:b])
                                    a = b + 1
                            d[cheie][l[0]].append(l[a:])
                    elif l[0] not in d[cheie]:
                        d[cheie].append(l[0])
    return d

def get_vars(d):
    cheie = "[Vars]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Variabilele nu au fost precizate!")
    return d[cheie]

def get_term(d):
    cheie = "[Term]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Terminalii nu au fost precizati!")
    return d[cheie]

def get_rules(d):
    cheie = "[Rules]"
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Regulile nu au fost precizate!")
    return d[cheie]

def generate_cfg(variabile, terminali, reguli):
    variabile1 = [variabile[0]]
    sir = []
    ok = 1
    while(ok):
        ok = 0
        variabile2 = []
        for i in range(0, len(variabile1)):
            x = random.randrange(len(reguli[variabile1[i]]))
            for j in range(0, len(reguli[variabile1[i]][x])):
                if reguli[variabile1[i]][x][j] in variabile:
                    variabile2.append(reguli[variabile1[i]][x][j])
                    ok = 1
                else:
                    sir.append(reguli[variabile1[i]][x][j])
        variabile1 = variabile2
    print(*sir)

d = get_section_list()
variabile = get_vars(d)
terminali = get_term(d)
reguli = get_rules(d)
generate_cfg(variabile, terminali, reguli)


