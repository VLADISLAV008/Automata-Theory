""" Developed the function that constructs an Eilenberg machine accepting exactly words corresponding
    to the input regular expression
"""
import queue
import json


class EilenbergMachine:
    """ Class representing Eilenberg machine.
        Constructor parameters are
            1.number_states: int -- the number of states of the Eilenberg machine
            2.transitions_between_states: list -- adjacency list of state transition.
                transitions_between_states[i] -- list of possible transitions from state i.
                    List items are tuples containing two items (s,a).
                    s -- number of the state to which it is possible to go from state i.
                    a -- the alphabet symbol corresponding to the transition from state i to state s.
            3.initial_states: list -- list of initial states.
            4.acceptable_states: list -- list of acceptable states.
        States are numbered starting at 0  and ending with number_states-1
    """

    def __init__(self, number_states: int, transitions_between_states: list,
                 initial_states: list, acceptable_states: list):
        self.number_states = number_states
        self.transitions_between_states = transitions_between_states
        self.initial_states = initial_states
        self.acceptable_states = acceptable_states

    def accept(self, expr: str) -> bool:
        """ The function distinguishes acceptable and non-acceptable input strings
            :param expr: str -- input string
            :return: acceptable and non-acceptable input strings
        """

        q = queue.Queue()
        for state in self.initial_states:
            q.put((state, expr))

        while not q.empty():
            state, expr = q.get()
            if expr == '':
                # if state is acceptable state then input string is acceptable
                if self.acceptable_states.__contains__(state):
                    return True
            else:
                # add to the queue all transitions from the state and corresponding to the symbol expr[0]
                for edge in self.transitions_between_states[state]:
                    if edge[1] == expr[0]:
                        q.put((edge[0], expr[1:]))
        return False

    @staticmethod
    def get_Eilenberg_machine(reg_expr: dict):
        """ Static function that returned Eilenberg machine
            accepting exactly words corresponding to the input regular expression.
            :param reg_expr: dict - the regular expression represented in JSON format in dict.
            :returns: EilenbergMachine -- resulting Eilenberg machine
        """

        key = reg_expr['key']
        value = reg_expr['val']

        if key == 'atm':
            return EilenbergMachine(2, [[(1, value)], []], [0], [1])
        elif key == '*':
            return EilenbergMachine._build_Eilenberg_machine_oper_asterisk(value)
        elif key == '.':
            return EilenbergMachine._build_Eilenberg_machine_oper_concat(value['fst'], value['snd'])
        elif key == '|':
            return EilenbergMachine._build_Eilenberg_machine_oper_or(value['fst'], value['snd'])

    @staticmethod
    def _build_Eilenberg_machine_oper_asterisk(reg_expr: dict):
        """ This private static function return the Eilenberg machine accepting exactly words
            corresponding to the regular expression "reg_expr_left*"
            :param reg_expr: dict -- argument of a unary operation *
            :return: EilenbergMachine -- resulting Eilenberg machine accepting exactly words
                corresponding to the regular expression "reg_expr*"
        """
        # Eilenberg machine for regular expression value
        e_machine = EilenbergMachine.get_Eilenberg_machine(reg_expr)

        # for all states leading to acceptable states,
        # we add transitions to the initial states with the corresponding symbol
        for s in range(e_machine.number_states):
            for (state, character) in e_machine.transitions_between_states[s]:
                # if 's' leading to acceptable state 'state' then
                # add transitions to all initial states with the corresponding symbol
                if e_machine.acceptable_states.__contains__(state):
                    for init_state in e_machine.initial_states:
                        e_machine.transitions_between_states[s].append((init_state, character))
        return e_machine

    @staticmethod
    def _build_Eilenberg_machine_oper_concat(reg_expr_left: dict, reg_expr_right: dict):
        """ This private static function return the Eilenberg machine accepting exactly words
            corresponding to the regular expression "reg_expr_left.reg_expr_right"
            :param reg_expr_left: dict -- first argument of a binary operation .
            :param reg_expr_right: dict -- second argument of a binary operation .
            :return: EilenbergMachine -- resulting Eilenberg machine accepting exactly words
                corresponding to the regular expression "reg_expr_left.reg_expr_right"
        """
        # Eilenberg machine for regular expression,
        # which is the first argument of the operation '.'.
        machine_fst = EilenbergMachine.get_Eilenberg_machine(reg_expr_left)

        # Eilenberg machine for regular expression,
        # which is the second argument of the operation '.'.
        machine_snd = EilenbergMachine.get_Eilenberg_machine(reg_expr_right)

        # the number of states of resulting Eilenberg machine
        number_states = \
            machine_fst.number_states + machine_snd.number_states - len(machine_snd.initial_states)

        # The dictionary contains pairs:
        # the old number of state (not including initial states) in the Eilenberg machine_snd and
        # the new number of state in the resulting Eilenberg machine
        new_state_numbers = {}
        # new_state_numbers is being filled (renumbering of states of Eilenberg machine_snd)
        new_number = machine_fst.number_states
        for s in range(machine_snd.number_states):
            if not machine_snd.initial_states.__contains__(s):
                new_state_numbers[s] = new_number
                new_number += 1

        # adjacency list of state transition of resulting Eilenberg machine
        transitions_between_states = machine_fst.transitions_between_states
        for i in range(machine_snd.number_states - len(machine_snd.initial_states)):
            transitions_between_states.append([])

        # Adding renumbered transitions between the states of the second machine to the resulting Eilenberg machine.
        # All transitions containing the initial states of the second machine are replaced by transitions containing,
        # instead of the initial state, the acceptable states of the first machine.
        for s in range(machine_snd.number_states):
            for (state, character) in machine_snd.transitions_between_states[s]:
                # the transition corresponding to a transition between an initial state and a non-initial state
                if machine_snd.initial_states.__contains__(s) and not machine_snd.initial_states.__contains__(state):
                    for act_s in machine_fst.acceptable_states:
                        transitions_between_states[act_s].append((new_state_numbers[state], character))
                # the transition corresponding to a transition between an initial state and an initial one
                elif machine_snd.initial_states.__contains__(s) and machine_snd.initial_states.__contains__(state):
                    for act_s in machine_fst.acceptable_states:
                        transitions_between_states[act_s].append((act_s, character))
                # the transition corresponding to a transition between a non-initial state and an initial state.
                elif not machine_snd.initial_states.__contains__(s) and machine_snd.initial_states.__contains__(state):
                    for act_s in machine_fst.acceptable_states:
                        transitions_between_states[new_state_numbers[s]].append((act_s, character))
                # the transition corresponding to a transition between a non-initial state and a non-initial state.
                elif not machine_snd.initial_states.__contains__(s) and \
                        not machine_snd.initial_states.__contains__(state):
                    transitions_between_states[new_state_numbers[s]].append((new_state_numbers[state], character))

        # the list of initial states of resulting Eilenberg machine
        initial_states = machine_fst.initial_states

        # the list of acceptable states of resulting Eilenberg machine
        acceptable_states = []
        # add all renumbered acceptable states of the machine_snd
        for s in machine_snd.acceptable_states:
            acceptable_states.append(new_state_numbers[s])

        return EilenbergMachine(number_states, transitions_between_states, initial_states, acceptable_states)

    @staticmethod
    def _build_Eilenberg_machine_oper_or(reg_expr_left: dict, reg_expr_right: dict):
        """ This private static function return the Eilenberg machine accepting exactly words
            corresponding to the regular expression "reg_expr_left|reg_expr_right"
            :param reg_expr_left: dict -- first argument of a binary operation |
            :param reg_expr_right: dict -- second argument of a binary operation |
            :return: EilenbergMachine -- resulting Eilenberg machine accepting exactly words
                corresponding to the regular expression "reg_expr_left|reg_expr_right"
        """
        # Eilenberg machine for regular expression,
        # which is the first argument of the operation '|'.
        machine_fst = EilenbergMachine.get_Eilenberg_machine(reg_expr_left)

        # Eilenberg machine for regular expression,
        # which is the second argument of the operation '|'.
        machine_snd = EilenbergMachine.get_Eilenberg_machine(reg_expr_right)

        # the number of states of resulting Eilenberg machine
        number_states = \
            machine_fst.number_states + machine_snd.number_states

        # adjacency list of state transition of resulting Eilenberg machine
        transitions_between_states = machine_fst.transitions_between_states
        for i in range(machine_snd.number_states):
            transitions_between_states.append([])

        # Adding renumbered transitions between the states of the second machine to the resulting Eilenberg machine.
        for s in range(machine_snd.number_states):
            for (state, character) in machine_snd.transitions_between_states[s]:
                transitions_between_states[s + machine_fst.number_states] \
                    .append((state + machine_fst.number_states, character))

        # the list of initial states of resulting Eilenberg machine
        initial_states = machine_fst.initial_states
        # add all renumbered initial states of the machine_snd
        for s in machine_snd.initial_states:
           initial_states.append(s + machine_fst.number_states)

        # the list of acceptable states of resulting Eilenberg machine
        acceptable_states = machine_fst.acceptable_states
        # add all renumbered acceptable states of the machine_snd
        for s in machine_snd.acceptable_states:
            acceptable_states.append(s + machine_fst.number_states)

        return EilenbergMachine(number_states, transitions_between_states, initial_states, acceptable_states)


def get_data_from_json_file(name_file: str) -> dict:
    """ The function reads the regular expression represented in JSON format.
        :param name_file: str -- the name of the file
        :return: decoded regular expression
    """
    with open(name_file, "r") as read_file:
        return json.load(read_file)


""" 
    Testing of Eilenberg machine
    Testing regular expression is ((a|b*)*.((d*.e)|c)).(b|a)*
"""
reg_expr_test = get_data_from_json_file("reg_expr_test.json")
machine = EilenbergMachine.get_Eilenberg_machine(reg_expr_test)

print(machine.accept("ac"))  # False
print(machine.accept("bbbda"))  # False
print(machine.accept(""))  # False
print(machine.accept("bbabbda"))  # False
print(machine.accept("abab"))  # False
print(machine.accept("addeca"))  # False
print(machine.accept("abbddeaaab"))  # True
print(machine.accept("aca"))  # True
print(machine.accept("bdea"))  # True
print(machine.accept("bbcbb"))  # True
