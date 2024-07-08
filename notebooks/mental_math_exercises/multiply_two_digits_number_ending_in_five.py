import numpy as np

from problem import Problem

class Multiply_two_digits_number_ending_in_five(Problem):

    def check_solution(self):
        if self.user_input == self.solution:
            print("Correct!\n")
        else:
            print(f"The correct solution was {self.solution}.\n")

    def generate_problem(self):
        self.random_int = np.random.randint(11 // 10, 90 // 10 + 1) * 10 + 5
        self.solution = self.random_int ** 2

    def print_problem(self):
        self.generate_problem()
        self.get_user_input(f"{self.random_int} * {self.random_int}\n")
        self.check_solution()


    def print_instructions(self):
        instructions = "Multiply an integer of 2 digits ending with 5 by itself is quite easy, let's make some examples: "\
        "\nexample 1: 35 * 35 = 1225 -> the two leftmost digits are 12. This is obtained by multiplying the"\
        "\nleftmost digit of the number (3) by itself + 1 (4) -> 3 * 4 = 12. "\
        "\nThen the remaining digits are simply 25. This results in 1225.\n"\
        "\nexample 2: 95 * 95 = 9025 -> again 9 * 10 = 90, then the last two digits are 25.\n"


        print_instructions = input("Do you want to read the instructions? (y/n)")
        if print_instructions == 'y':
            print(instructions)

    @staticmethod
    def return_exercise_type():
        return "Power of 2 of a two digit number ending in 5"
