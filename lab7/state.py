class State:
    def __init__(self):
        self.out = {}
        self.is_it_end = False
        self.char_class = {}

    def check_string(self, string):
        return self.next_step(string)

    def next_step(self, string):
        if '$' in self.out:
            if self.out['$'].next_step(string):
                return True
        if '&' in self.out:
            if self.out['&'].next_step(string):
                return True
        if not string:
            if self.is_it_end:
                return True
            else:
                return False
        first_char, tail = string[0], string[1:]
        if first_char in self.out:
            if self.out[first_char].next_step(tail):
                return True
        if '.' in self.out:
            if self.out['.'].next_step(tail):
                return True
        for k, v in self.char_class.items():
            if k[0] == '\\':
                if k == '\\d' and '0' <= first_char <= '9' and v.next_step(tail):
                    return True
                elif k == '\\D' and (first_char > '9' or first_char < '0') and v.next_step(tail):
                    return True
                elif k == '\\w' and (('0' <= first_char <= '9') or ('a' <= first_char <= 'z') or
                                     ('A' <= first_char <= 'Z')) and v.next_step(tail):
                    return True
            elif first_char in k and v.next_step(tail):
                return True
        return False

    def add_next_states(self, regex, final_state=None):
        if not regex:
            if final_state:
                self.out['$'] = final_state
            else:
                self.is_it_end = True
            return
        if len(regex) > 1 and regex[1] in ['+', '?', '*']:
            next_fragment, tail = regex[:2], regex[2:]

            if next_fragment[-1] == '+':
                middle_state = State()
                next_state = State()
                middle_state.out[next_fragment[0]] = middle_state
                middle_state.out['$'] = next_state

                self.out[next_fragment[0]] = middle_state
                next_state.add_next_states(tail, final_state)
            elif next_fragment[-1] == '?':
                state0 = State()
                state1 = State()
                self.out['$'] = state0
                self.out[next_fragment[0]] = state1

                state0.add_next_states(tail, final_state)
                state1.add_next_states(tail, final_state)
            elif next_fragment[-1] == '*':
                state0 = State()
                state1 = State()

                self.out[next_fragment[0]] = state1
                self.out['$'] = state0

                state1.out['$'] = self
                state0.add_next_states(tail, final_state)
        elif regex[0] != '[' and regex[0] != '(':
            next_state = State()
            self.out[regex[0]] = next_state
            next_state.add_next_states(regex[1:], final_state)
        elif regex[0] == '[':
            end = 0
            while regex[end] != ']':
                end += 1
            inside = regex[1:end]
            if len(regex) > end + 1 and regex[end + 1] in ['*', '+', '?']:
                tail = regex[end + 2:]
                special_char = regex[end + 1]
                if special_char == '+':
                    middle_state = State()
                    next_state = State()
                    middle_state.char_class[inside] = middle_state
                    middle_state.out['$'] = next_state

                    self.char_class[inside] = middle_state
                    next_state.add_next_states(tail, final_state)
                elif special_char == '?':
                    state0 = State()
                    state1 = State()
                    self.out['$'] = state0
                    self.char_class[inside] = state1

                    state0.add_next_states(tail, final_state)
                    state1.add_next_states(tail, final_state)
                elif special_char == '*':
                    state0 = State()
                    state1 = State()

                    self.char_class[inside] = state1
                    self.out['$'] = state0

                    state1.out['$'] = self
                    state0.add_next_states(tail, final_state)
            else:
                next_state = State()
                self.char_class[inside] = next_state
                next_state.add_next_states(regex[end + 1:], final_state)
        elif regex[0] == '(':
            number_of_not_closed_brackets = 1
            i = 0
            while number_of_not_closed_brackets > 0:
                i += 1
                if regex[i] == ')':
                    number_of_not_closed_brackets -= 1
                elif regex[i] == '(':
                    number_of_not_closed_brackets += 1

            inside = regex[1:i]
            if len(regex) > i + 1 and regex[i + 1] in ['+', '*', '?']:
                regex = regex[i + 1:]

                if regex[0] == '+':
                    end_state = State()
                    next_state = State()
                    next_state.add_next_states(inside, end_state)
                    final_state.out['$'] = self
                    final_state.add_next_states(regex[1:], final_state)
                elif regex[0] == '*':
                    outside_state = State()
                    next_state = State()
                    next_state.add_next_states(inside, self)
                    self.out['$'] = next_state
                    next_state.out['&'] = outside_state
                    outside_state.add_next_states(regex[1:], final_state)
                elif regex[0] == '?':
                    state0 = State()
                    state1 = State()

                    next_state = State()
                    self.out['$'] = next_state
                    next_state.add_next_states(inside, state1)
                    next_state.out['&'] = state0
                    state0.add_next_states(regex[1:], final_state)
                    state1.add_next_states(regex[1:], final_state)
            else:
                print(regex, regex[i + 1:])
                outside_state = State()
                next_state = State()
                next_state.add_next_states(inside, outside_state)
                self.out['$'] = next_state
                outside_state.add_next_states(regex[i + 1:], final_state)

    def __str__(self):
        return str(self.out) + '\n' + str(self.char_class)


def create_finite_automaton(regex):
    start = State()
    start.add_next_states(regex)
    return start
