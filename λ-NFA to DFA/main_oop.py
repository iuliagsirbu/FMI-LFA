import subprocess


class NFA:
    def __init__(self, filename):
        self.alphabet = []
        self.states = {}
        self.final_states = []
        self.closure = {}
        self.read_file(filename)
        self.compute_closures()

    def read_file(self, filename):
        with open(filename, "r") as f:
            lines = [line.strip().split() for line in f.readlines()]

        self.alphabet = lines[0]
        self.final_states = lines[-1]
        lines = lines[1:-1]

        # we want our dictionary to look like this:
        # {'0': [['a', ['0', '1']], ['b', ['2']], ['l', ['3', '2']]] ... }

        for line in lines:
            if line[0] not in self.states:
                self.states[line[0]] = [[line[1], [line[2]]]]
                if line[2] != line[0]:
                    self.states[line[2]] = []
            else:
                check = False
                for i in range(len(self.states[line[0]])):
                    aux = self.states[line[0]][i]
                    if aux[0] == line[1]:
                        check = True
                        aux[1].append(line[2])
                        if line[2] not in self.states:
                            self.states[line[2]] = []
                if not check:
                    self.states[line[0]].append([line[1], [line[2]]])
                    if line[2] not in self.states:
                        self.states[line[2]] = []
        # print(self.states)

    def compute_closures(self):
        # now we need the lambda (or epsilon) closures of each state
        # we want our dictionary to look like this:
        # {'0': ['0', '2', '3', '4', '5', '6'], ...}
        for state in self.states:
            check = False
            for letter in self.states[state]:
                if letter[0] == 'l':
                    check = True
                    if state not in self.closure:
                        self.closure[state] = letter[1].copy()

            if not check:
                self.closure[state] = [state]
            else:
                self.closure[state].append(state)

        # we now complete the lambda (or epsilon) closures for each state
        for state in self.closure:
            to_check = self.closure[state]
            for path in to_check:
                for path_ in self.closure[path]:
                    if path_ not in to_check:
                        to_check.append(path_)
            self.closure[state].sort()

        # print(self.closure)

# construction of the AFD
# we aim for a dictionary like the first one
# the start is the lambda (or epsilon) closure of the first state


class DFA:
    def __init__(self, nfa):
        self.alphabet = nfa.alphabet
        self.states = nfa.states
        self.final_states = []
        self.start = nfa.closure[list(nfa.closure.keys())[0]]
        self.automata = {}
        self.compute_states(nfa)

    def compute_states(self, nfa):
        key = ""
        for path in nfa.closure[list(nfa.closure.keys())[0]]:
            key += f"q{path}"
        loop = [key]
        for key in loop:
            self.automata[key] = []
            self.start = key.replace("q", " ")
            self.start = self.start.strip().split(" ")
            # print(key, self.start, sep='\n')
            for letter in self.alphabet:
                if letter != 'l':
                    aux = set()
                    letter_afd = set()
                    new_key = ""
                    for step in self.start:
                        for path in self.states[step]:
                            if path[0] == letter:
                                aux.update(path[1])
                    for path in aux:
                        if path in nfa.closure:
                            letter_afd.update(nfa.closure[path])
                    for path in sorted(letter_afd):
                        new_key += f"q{path}"
                    if new_key not in loop:
                        if new_key != '':
                            loop.append(new_key)
                    if len(letter_afd) != 0:
                        self.automata[key].append([letter, sorted(letter_afd)])

        print(self.automata)

        for key in self.automata:
            for state in nfa.final_states:
                if state in key.replace("q", " ").strip().split(" ") and key not in self.final_states:
                    self.final_states.append(key)

    def write_to_file(self, filename):
        with open(filename, "w") as g:
            g = open(filename, "w")
            g.write("""digraph finite_state_machine {
            fontname="Helvetica, Arial, sans-serif"
            node[fontname="Helvetica,Arial,sans-serif"]
            edge[fontname="Helvetica,Arial,sans-serif"]
            rankdir=LR;
            node [shape = doublecircle]; """
                    )
            g.write(f"{' '.join(self.final_states)};\n")
            g.write("node [shape = circle];\n")
            for key in self.automata:
                for transition in self.automata[key]:
                    g.write(
                        f"""{key} -> {'q' + 'q'.join(transition[1])} [label = "{transition[0]}"];\n""")
            g.write("}")

    def write_to_png(self):
        input_file = 'DFA.dot'
        output_file = 'DFA.png'

        subprocess.run(['dot', '-Tpng', input_file,
                       '-o', output_file], check=True)


nfa = NFA("input.txt")
dfa = DFA(nfa)
dfa.write_to_file("DFA.dot")
dfa.write_to_png()
