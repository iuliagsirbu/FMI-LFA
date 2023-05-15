import subprocess

f = open("input.txt", "r")
lines = []
for line in f:
    # we process the data from the file
    lines += [line.strip().split()]
alphabet = lines[0]
final_states = lines[-1]
lines = lines[1:-1]
f.close()
# we want our dictionary to look like this:
# {'0': [['a', ['0', '1']], ['b', ['2']], ['l', ['3', '2']]] ... }
states = {}
for line in lines:
    if line[0] not in states:
        states[line[0]] = [[line[1], [line[2]]]]
        if line[2] != line[0]:
            states[line[2]] = []
    else:
        check = 0
        for i in range(len(states[line[0]])):
            aux = states[line[0]][i]
            if aux[0] == line[1]:
                check = 1
                aux[1].append(line[2])
                if line[2] not in states:
                    states[line[2]] = []
        if check == 0:
            states[line[0]].append([line[1], [line[2]]])
            if line[2] not in states:
                states[line[2]] = []

# now we need the lambda (or epsilon) closures of each state
# we want our dictionary to look like this:
# {'0': ['0', '2', '3', '4', '5', '6'], ...}
closure = {}
for state in states:
    check = 0
    for letter in states[state]:
        if letter[0] == 'l':
            check = 1
            if state not in closure:
                closure[state] = letter[1].copy()
            # else:
            #     closure[state].append(letter[1])
    if check == 0:
        closure[state] = [state]
    else:
        closure[state].append(state)

# we now complete the lambda (or epsilon) closures for each state
for state in closure:
    to_check = closure[state]
    for path in to_check:
        for path_ in closure[path]:
            if path_ not in to_check:
                to_check.append(path_)
    closure[state].sort()
print(closure)
# construction of the AFD
# we aim for a dictionary like the first one
# the start is the lambda (or epsilon) closure of the first state
DFA = {}
key = ""
for path in closure[list(closure.keys())[0]]:
    key += f"q{path}"
start = closure[list(closure.keys())[0]]
loop = [key]

for key in loop:
    DFA[key] = []
    start = key.replace("q", " ")
    start = start.strip().split(" ")
    # print(key, start, sep="\n")
    for letter in alphabet:
        if letter != 'l':
            aux = set()
            letter_afd = set()
            new_key = ""
            for step in start:
                # print(key, start, step)
                for path in states[step]:
                    if path[0] == letter:
                        aux.update(path[1])
            for path in aux:
                if path in closure:
                    letter_afd.update(closure[path])
            for path in sorted(letter_afd):
                new_key += f"q{path}"
            if new_key not in loop:
                if new_key != '':
                    loop.append(new_key)
            if len(letter_afd) != 0:
                DFA[key].append([letter, sorted(letter_afd)])
DFA_fstates = []
# the final states of the DFA are those who contain at least one final state from the initial lambda (or epsilon) NFA
for key in DFA:
    for state in final_states:
        if state in key.replace("q", " ").strip().split(" ") and key not in DFA_fstates:
            DFA_fstates.append(key)
print(DFA)
g = open("DFA.dot", "w")
g.write("""digraph finite_state_machine {
        fontname="Helvetica, Arial, sans-serif"
        node[fontname="Helvetica,Arial,sans-serif"]
        edge[fontname="Helvetica,Arial,sans-serif"]
        rankdir=LR;
        node [shape = doublecircle]; """
        )
g.write(f"{' '.join(DFA_fstates)};\n")
g.write("node [shape = circle];\n")
for key in DFA:
    for transition in DFA[key]:
        g.write(
            f"""{key} -> {'q' + 'q'.join(transition[1])} [label = "{transition[0]}"];\n""")
g.write("}")
g.close()

# script to output the DFA using Graphviz as a png
input_file = 'DFA.dot'
output_file = 'DFA.png'

subprocess.run(['dot', '-Tpng', input_file, '-o', output_file], check=True)
