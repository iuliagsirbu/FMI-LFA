# pentru o gramatica regulata, genereaza toate cuvintele de o lungime n
f = open("input.txt", "r")
n = int(f.readline())
grammar = {}
# grammar retine gramatica pentru prelucrare
for line in f:
    line = line.strip().split()
    if line[0] not in grammar:
        grammar[line[0]] = line[1:]
# S = start
words = []  # stocam cuvintele pe masura ce sunt generate
start = 0
for i in range(n):
    # daca deja am inceput prelucrarea
    if start != 0:
        words2 = []  # se creeaza o lista temporara in care stocam noile cuvinte formate
        for cuvant in words:
            if cuvant[-1] != "λ" and (cuvant[-1] >= "A" and cuvant[-1] <= "Z"):
                # daca urmatoarea stare este una care poate fi prelucrabila
                lista = grammar[cuvant[-1]]  # preiau din dictionar starile
            else:
                continue
            for stare in lista:  # pentru fiecare stare preluata
                cuvant2 = cuvant[:-1] + stare  # formez noul cuvant
                words2.append(cuvant2)  # adaug in lista temporara
        words = words2  # actualizez lista cu noile cuvinte
    # daca nu am inceput prelucrarea
    if start == 0:  # daca nu a fost accesat Start
        lista = grammar["S"]
        for stare in lista:
            words.append(stare)  # lista contine cuvintele pentru Start
        start = 1
final = []  # lista finala, dupa validare

# VALIDARE CUVINTE
# print(words)
for word in words:
    # print(word)
    if word[-1] == "λ":  # daca a ajuns intr-o stare finala - lambda
        if len(word) - 1 == n:  # daca are lungimea necesara
            final.append(word)
    if word[-1] >= "a" and word[-1] <= "z":  # daca a ajuns intr-o stare finala
        final.append(word)
    elif word[-1] >= "A" and word[-1] <= "Z":
        # daca a ajuns intr-o stare potential finala
        list = grammar[word[-1]]
        if "λ" in list:  # daca lambda este printre stari, cuvantul este valid
            final.append(word[:-1])
print(*final)
