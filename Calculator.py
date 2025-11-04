from dataclasses import dataclass

'''
STATE FUNCTIONALITY AND LIMITIATIONS:

FIRST_STATE: 
Any number input is stored in the last_num list. Numbers or the 
operator may be pressed during this state. Begins when the 
application is opened, ends once an operator, then a number is hit.

SECOND_STATE:
Any number will be stored in the second_num list. Numbers or the 
equals sign may be pressed during this state. Begins when a number is hit
after operator input, ends when the equal sign is pressed.

RESULT_STATE:
Clear button opens up. Another operator can be set to chain equations. 
No new numbers can be set until operator is set. Begins when
the equal sign is pressed, ends when either:

1. Operator, then number selected --> SECOND_STATE
2. Clear button pressed --> FIRST_STATE

ERROR_STATE:
Alternative RESULT_STATE that happens when a divide by zero happens. The
only way out is to hit the "CLEAR" button to return back to FIRST_STATE

'''

@dataclass
class Calculator:
    calc_history = ['']
    last_num = [0]
    second_num = [0]
    operator = ''
    first_num_set = False
    second_num_set = False
    divide_by_zero = False

# -------------- STATE MANAGEMENT ---------------------------------------------- #

    # Used to set states manually. Raw booleans are never touched directly
    def set_state(self, state):

        states = { # (first, second)
            "FIRST_STATE": (False, False, False),
            "SECOND_STATE": (True, False, False),
            "RESULT_STATE": (True, True, False),
            "ERROR_STATE": (True, True, True)
        }

        key = state
        handler = states.get(key)
        if handler:
           self.first_num_set, self.second_num_set, self.divide_by_zero = handler

    # Handles state verification; seeing where we are at any given moment
    def check_state(self):

        states = { #(first, second)
            (False, False, False): "FIRST_STATE",
            (True, False, False): "SECOND_STATE",
            (True, True, False): "RESULT_STATE",
            (True, True, True): "ERROR_STATE"
        }

        key = (self.first_num_set, self.second_num_set, self.divide_by_zero)
        handler = states.get(key)
        if handler:
            return handler

# --------------- CORE LOGIC ------------------------------------------------- #

    # Actual appending
    def build_number(self, num: int, number_list: list[str]):
        number_list.append(num)

    # Checking where to put each number and what to combine
    def set_number(self, number):
        match self.check_state():
            case "FIRST_STATE":
                self.build_number(number, self.last_num)
            case "SECOND_STATE":
                self.build_number(number, self.second_num)

    # Very important function to turn the list of string digits into a number
    def combine_number(self, number: list[str]):
        combined_number = ''
        for n in number:
            combined_number+=str(n)
        if '.' in combined_number:
            return float(combined_number)
        elif combined_number == '':
            return 0
        else:
            return int(combined_number)

    # Mainly for the GUI to know what to display
    def get_display_text(self, number):
        match self.check_state():
            case "FIRST_STATE":
                self.set_number(number)
                return self.combine_number(self.last_num)
            case "SECOND_STATE":
                self.set_number(number)
                return self.combine_number(self.second_num)

    # We take the last equation and add it to the calculation history
    def set_history(self, first, second):
        last_equation = f'{first} {self.operator} {second} = {self.last_num}'
        self.calc_history.append(last_equation)

    def reset(self):
        self.second_num = [0]

    def set_operator(self, operator: str):
       self.operator = operator
       self.set_state("SECOND_STATE")


    # See if the parameter is an integer or float, because if it is, we cannot combine it
    def get_value(self, num):
        if isinstance(num, (int, float)):
            return num
        return self.combine_number(num)


# --------------- CALCULATION -------------------------------------------- #


    def basic_calc(self):
        self.set_state("RESULT_STATE")

        first = self.get_value(self.last_num)
        second = self.get_value(self.second_num)

        try:
            self.last_num = eval(f'{first} {self.operator} {second}')
            self.set_history(first, second)
            self.reset()
        except ZeroDivisionError:
            self.set_state("ERROR_STATE")
            return 'Error:\n Divison by Zero'
        return self.last_num

# ------------------ UTILITIES --------------------------------------------------- #

    # Completely resets things, as if you'd just opened the application
    def clear(self):
        self.last_num = [0]
        self.second_num = [0]
        operator = ''
        self.set_state('FIRST_STATE')
        return 0

    # The main function to delete digits
    def take_away(self, number: list[str]):
        if not number:
            number = [0]
            return self.combine_number(number)
        else:
            number.pop(len(number) - 1)
            return self.combine_number(number)

    def delete(self):
        current_state = self.check_state()

        if current_state in ('ERROR_STATE', 'RESULT_STATE'):
            print('clearing')
            return self.clear()

        if current_state == 'FIRST_STATE':
            self.take_away(self.last_num)
            return self.get_value(self.last_num)

        if current_state == 'SECOND_STATE':
            self.take_away(self.second_num)
            if self.second_num == [0]:
                # No more digits in the second number --> switch to operator
                return self.operator
            if self.second_num == []:
                # Where we delete the operator and go back to FIRST_STATE
                self.set_state('FIRST_STATE')
                if isinstance(self.last_num, (int, float)):
                    self.set_state('RESULT_STATE')
                    return self.last_num
                self.operator = ''
                return self.combine_number(self.last_num)
        return self.combine_number(self.second_num)
