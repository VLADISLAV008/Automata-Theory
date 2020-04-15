""" Two functions is implemented:
        for eliminating unreachable states of a deterministic finite state machine
        for reducing a deterministic finite state machine
"""

import queue


class DFSM:
    """ Class representing deterministic finite state machine.
        Constructor parameters are
            1.alphabet: list -- list of symbols of the alphabet.
            2.number_states: int -- the number of states of the DFSM
            3.transitions_between_states: list -- adjacency list of state transition.
                transitions_between_states[i] -- list of possible transitions from state i.
                    List items are tuples containing two items (s,a).
                    s -- number of the state to which it is possible to go from state i.
                    a -- the alphabet symbol corresponding to the transition from state i to state s.
            4.initial_state: int -- number of the initial state of the DFSM.
            5.acceptable_states: list -- list of acceptable states.
        States are numbered starting at 0  and ending with number_states - 1
    """

    def __init__(self, alphabet: list, number_states: int, transitions_between_states: list,
                 initial_state: int, acceptable_states: list):
        self.alphabet = alphabet
        self.number_states = number_states
        self.transitions_between_states = transitions_between_states
        self.initial_state = initial_state
        self.acceptable_states = acceptable_states

    def _transition(self, state: int, char: str) -> int:
        for (s, c) in self.transitions_between_states[state]:
            if c == char:
                return s
        return -1

    def eliminate_unreachable_states(self):
        """ The function eliminate unreachable states of
            the deterministic finite state machine
        """

        used = [False] * self.number_states

        q = queue.Queue()
        q.put(self.initial_state)
        used[self.initial_state] = True

        while not q.empty():
            state = q.get()
            for (s, c) in self.transitions_between_states[state]:
                if not used[s]:
                    used[s] = True
                    q.put(s)

        # The dictionary contains pairs:
        # the old number of state, not including unreachable states and
        # the new number of state in the resulting DFSM
        new_state_numbers = {}
        # new_state_numbers is being filled (renumbering of states of DFSM)
        new_number = 0
        for s in range(self.number_states):
            if used[s]:
                new_state_numbers[s] = new_number
                new_number += 1

        new_transitions_between_states = []
        for i in range(new_number):
            new_transitions_between_states.append([])
        for s in range(self.number_states):
            if used[s]:
                for (state, char) in self.transitions_between_states[s]:
                    if used[state]:
                        new_transitions_between_states[new_state_numbers[s]].append((new_state_numbers[state], char))
        self.transitions_between_states = new_transitions_between_states

        self.number_states = new_number

        self.initial_state = new_state_numbers[self.initial_state]

        new_acceptable_states = []
        for s in self.acceptable_states:
            if used[s]:
                new_acceptable_states.append(new_state_numbers[s])
        self.acceptable_states = new_acceptable_states

    def reduce_dfsm(self):
        """ The function reduce a deterministic finite state machine """
        # list of not acceptable states
        not_acceptable_states = []
        for i in range(self.number_states):
            if not self.acceptable_states.__contains__(i):
                not_acceptable_states.append(i)

        # list splitting multiple states
        # initial splitting of a set of states - a class of admitting states and a class of inadmissible states
        classes = [self.acceptable_states.copy(), not_acceptable_states]

        q = queue.Queue()
        for c in self.alphabet:
            q.put((classes[0], c))
            q.put((classes[1], c))

        while not q.empty():
            set_states, char = q.get()
            set_states: list
            for s in classes:
                set_fst = []
                set_snd = []
                for state in s:
                    to_state = self._transition(state, char)
                    if to_state == -1 or not set_states.__contains__(to_state):
                        set_snd.append(state)
                    else:
                        set_fst.append(state)
                if not len(set_fst) == 0 and not len(set_snd) == 0:
                    classes.remove(s)
                    classes.append(set_fst)
                    classes.append(set_snd)
                    for c in self.alphabet:
                        q.put((set_fst, c))
                        q.put((set_snd, c))

        # The dictionary contains pairs:
        # the old number of state and
        # the new number of state in the resulting DFSM
        new_state_numbers = {}
        # new_state_numbers is being filled (renumbering of states of DFSM)
        new_number = 0
        for s in classes:
            for state in s:
                new_state_numbers[state] = new_number
            new_number += 1

        new_transitions_between_states = []
        for i in range(new_number):
            new_transitions_between_states.append([])
        for s in range(self.number_states):
            for (state, char) in self.transitions_between_states[s]:
                if not new_transitions_between_states[new_state_numbers[s]].__contains__(
                        (new_state_numbers[state], char)):
                    new_transitions_between_states[new_state_numbers[s]].append((new_state_numbers[state], char))
        self.transitions_between_states = new_transitions_between_states

        self.number_states = new_number

        self.initial_state = new_state_numbers[self.initial_state]

        new_acceptable_states = []
        for s in self.acceptable_states:
            if not new_acceptable_states.__contains__(new_state_numbers[s]):
                new_acceptable_states.append(new_state_numbers[s])
        self.acceptable_states = new_acceptable_states


""" 
    Testing class DFSM
"""

machine = DFSM(['a', 'b', 'c'], 5, [[(1, 'a'), (3, 'b')], [(4, 'c')], [(1, 'b')], [(4, 'c')], []], 0, [4])

machine.eliminate_unreachable_states()

print(machine.number_states)
print(machine.transitions_between_states)
print(machine.initial_state)
print(machine.acceptable_states)

print("=======================")
machine.reduce_dfsm()
print(machine.number_states)
print(machine.transitions_between_states)
print(machine.initial_state)
print(machine.acceptable_states)
