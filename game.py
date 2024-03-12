#student: Capitanu Andreea
#grupa: 143
fin = open("game.in", "r")

#pentru a ne folosi de LA in realizarea jocului nostru,
#(a se vedea in fisierul de intrare game.in) am considerat camerele ca fiind starile automatului
#alfabetul este dat de actiuni (precum go),
#alfabetul listei sunt itemele
#si conditia necesara de intrare intr-o camera se realizeaza exact cu verificarea daca
#itemul apare in inventarul jucatorului.

#pentru validarea optiunilor, acestea au fost scrise in cfg.in,
#iar programul cfg.py genereaza astfel de optiuni

#am preluat functiile definite si explicate anterior pentru LA
def get_section_list():
    l = []
    d = {}
    for linie in fin:
        linie = linie.replace(",", " ")
        linie = linie.replace("->", " ")
        linie = linie.replace("(", " ")
        linie = linie.replace(")", " ")
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
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul nu a fost precizat!")
    return d[cheie]

def get_gamma(d):
    cheie = "[Gamma]"
    d[cheie] = set(d[cheie])
    d[cheie].add('e')
    if cheie not in d.keys() or d[cheie] == []:
        raise Exception("Alfabetul listei nu a fost precizat!")
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
            raise Exception(f"Litera {x[2]} nu face parte din alfabetul definit pentru lista!")
        if x[3] not in stari:
            raise Exception(f"Starea {x[3]} nu este definita!")
        if x[4] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[4]} nu face parte din alfabetul definit pentru lista!")
        if x[5] not in d["[Gamma]"]:
            raise Exception(f"Litera {x[5]} nu face parte din alfabetul definit pentru lista!")
    return d[cheie]

d = get_section_list()
alfabet = get_sigma(d)
gamma = get_gamma(d)
stari, start, finale = get_states(d)
delta = get_delta(d)

#lista cuprinde optiunile posibile ale jucatorului
actions = ["look", "go", "take", "inventory", "drop item", "exit game"]
#current_room retine camera curenta in care se afla jucatorul
#si este initializata cu Entrance_Hall
current_room = start[0]
#lista inventar reprezinta inventarul jucatorului
inventar = []
#info_camere este un dictionar in care cheile sunt reprezentate de camerele castelului
#si cuprinde tat descrierea camerelor, cat si itemele ce se afla in fiecare camera
iteme_camere = {"Entrance_Hall": [["The grand foyer of the Castle of Illusions."], ["key"]],
                "Dining_Room": [["A room with a large table filled with an everlasting feast."], ["invitation", "chef's_hat"]],
                "Kitchen": [["A room packed with peculiar ingredients."], ["spoon"]],
                "Armoury": [["A chamber filled with antiquated weapons and armour."], ["sword", "crown"]],
                "Treasury": [["A glittering room overflowing with gold and gemstones."], ["ancient_coin"]],
                "Library": [["A vast repository of ancient and enchanted texts."], ["spell_book"]],
                "Pantry": [["A storage area for the Kitchen."], []],
                "Throne_Room": [["The command center of the castle."], []],
                "Wizard's_Study": [["A room teeming with mystical artifacts."], ["magic_wand"]],
                "Secret_Exit": [["The hidden passage that leads out of the Castle of Illusions."], []]}

#un mesaj de initiere a jucatorului in poveste
print("Howdy, fellow adventurer!\nAs you might see, we are trapped in the Castle of Illusions...\n"
      "In order to escape this place, we must find the Secret Exit!\nWhat shall we do?...")

#meniul este afisat cat timp jucatorul nu a gasit inca iesirea secreta
while(current_room != "Secret_Exit"):
    #retinem toate optiunile valabile in situatia curenta
    options = []
    print("\nOptions: ")
    #numarul curent al optiunii
    cnt = 0
    #AFISAREA OPTIUNILOR VALABILE
    #parcurgem lista cu actiunile posibile pentru jucator
    for i in range(len(actions)):
        #actiunea go
        if i == 1:
            for x in delta:
                if x[0] == current_room:
                    cnt = cnt + 1
                    #afisam camerele adiacente, in care se poate duce jucatorul
                    print(f"{cnt}. go {x[3]}")
                    options.append(["go", x[3]])
        elif i == 2:
            #actiunea take
            for x in iteme_camere[current_room][1]:
                cnt = cnt + 1
                #afisam itemele din camera curenta
                print(f"{cnt}. take {x}")
                options.append(["take", x])
        else:
            #afisam restul actiunilor posibile din lista
            cnt = cnt + 1
            print(f"{cnt}. {actions[i]}")
            options.append([actions[i]])

    #CITIREA OPTIUNII JUCATORULUI SI PRELUCRAREA DATELOR
    #retinem in val, numarul optiunii alese de jucator
    val = int(input("Write the number of the desired option: "))
    val = val - 1
    #afisam descrierea camerei
    if "look" == options[val][0]:
        print(f"{current_room}:", end = " ")
        print(*iteme_camere[current_room][0])
    #adaugam itemul in inventarul jucatorului si il stergem din cel al camerei
    elif "take" == options[val][0]:
        inventar.append(options[val][1])
        iteme_camere[current_room][1].remove(options[val][1])
    #afisam inventarul jucatorului
    elif "inventory" == options[val][0]:
        print("Your inventory: ", end = " ")
        print(*inventar)
    #afisam itemele din inventarul jucatorului
    #pentru a-si alege pe care il elimina
    elif "drop item" == options[val][0]:
        cntt = 0
        for x in inventar:
            cntt = cntt + 1
            print(f"{cntt}. {x}")
        vall = int(input("Choose the item you want to drop: "))
        #eliminam itemul din inventarul jucatorului
        #si il adaugam in cel al camerei
        iteme_camere[current_room][1].append(inventar[vall - 1])
        inventar.remove(inventar[vall - 1])
    #schimbam valoarea lui current_room
    elif "go" == options[val][0]:
        ok = 0
        for x in delta:
            if x[0] == current_room and x[3] == options[val][1]:
                #verificam daca este necesara detinerea vreunui item pentru a intra in camera
                if x[2] != 'e':
                    if x[2] in inventar:
                        ok = 1
                    else:
                        print(f"We need {x[2]} to enter {x[3]}")
                else:
                    ok = 1
        if ok == 1:
            current_room = options[val][1]
    #incheiem programul
    elif "exit game" == options[val][0]:
        print("Enjoy your eternity in the Castle of Illusions!")
        exit(0)

#afisarea unui mesaj de felicitare si de ramas bun
if current_room == "Secret_Exit":
    print("\nYou found the exit!\nLooks like this is the end of this journey, adventurer!")