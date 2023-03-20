def validator(cuvant, stari, starifinale):
    for stari_key, stari_value in stari.items():
        q = stari_key
        break
    drum = ["q" + str(q) + " (start)"]
    for lit in cuvant:  # pentru fiecare pas din cuvant
        found = 0
        for stare in stari[q]:  # cautam directia din starea actuala
            if stare[0] == lit:  # daca pasul corespunde cu o tranzitie
                q = stare[1]  # mutam starea
                found = 1  # tinem minte ca s-a gasit o tranzitie
                drum += ["q" + str(q)]
        if found == 0:  # daca nu s-a gasit o continuare
            print("invalid")
            break
    if q in starifinale:  # daca nu a fost declarat invalid in timpul prelucrarii,
        # ajunge intr-o presupusa stare finala care este verificata aici
        # tot aici se verifica si cuvantul vid
        print("valid si drumul este: {}".format(drum))
    else:  # chiar daca s-a terminat cuvantul intr-o stare, nu e una finala
        print("invalid")


f = open("automat.txt", "r")
lines = []
for line in f:
    # citim datele pentru automat din fisier
    lines = lines + [line.strip().split()]

stari = {}
# punem intr-un dictionar starile, si prelucram cu exceptia ultimei linii cu starile finale
for line in lines[:-1]:
    if line[0] not in stari:
        # fiecare stare tine minte tranzitia catre alta stare
        stari[line[0]] = [[line[1], line[2]]]
    else:
        # daca exista deja in dictionar, dar se mai citesc si alte drumuri, se adauga si ele in dictionar
        stari[line[0]] = stari[line[0]] + [[line[1], line[2]]]

# o lista cu starile finale pentru verificarea cuvantului
starifinale = lines[-1]
# citim cuvintele pentru validare
g = open("cuvinte.txt", "r")
for cuvant in g:
    validator(cuvant.strip(), stari, starifinale)
