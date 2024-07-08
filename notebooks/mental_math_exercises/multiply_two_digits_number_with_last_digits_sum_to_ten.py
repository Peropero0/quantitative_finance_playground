import numpy as np

from problem import Problem

class Multiply_two_digits_number_with_last_digits_sum_to_ten(Problem):

    def check_solution(self):
        if self.user_input == self.solution:
            print("Correct!\n")
        else:
            print(f"The correct solution was {self.solution}.\n")

    @staticmethod
    def generate_numbers():
        r = np.random.randint(1, 10)
        units1 = np.random.randint(0, 10)
        units2 = 10 - units1

        number1 = r * 10 + units1
        number2 = r * 10 + units2

        return number1, number2

    def generate_problem(self):
        self.random_int_1, self.random_int_2 = Multiply_two_digits_number_with_last_digits_sum_to_ten.generate_numbers()
        self.solution = self.random_int_1 * self.random_int_2

    def print_problem(self):
        self.generate_problem()
        self.get_user_input(f"{self.random_int_1} * {self.random_int_2}\n")
        self.check_solution()


    def print_instructions(self):
        instructions = "Here we want to multiply two 2 digits numbers with the same starting digit and ending digits summing to 10.\n"\
        "Example 1: 47 * 43 = 2021 -> Here we have that the starting digit of the \n"\
        "two numbers is the same (4) while the last digits sum to 10 (7 + 3).\n"\
        "The sum is obtained as follows: first two digits 20 = 4 * (4+1)\n"\
        "last two digits 21 = 7 * 3.\n"\
        "Example 2: 78 * 72 = 5616 -> 56 = 7 * (7+1), 16 = 8 * 2\n"


        print_instructions = input("Do you want to read the instructions? (y/n)")
        if print_instructions == 'y':
            print(instructions)

    @staticmethod
    def return_exercise_type():
        return "Multiply two 2 digits numbers with the same starting digit and eding digit summing to 10"
