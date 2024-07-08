import numpy as np

from problem import Problem

class Mult_by_eleven(Problem):

    def check_solution(self):
        if self.user_input == self.solution:
            print("Correct!\n")
        else:
            print(f"The correct solution was {self.solution}.\n")

    def generate_problem(self):
        self.random_int = np.random.randint(12, 100)
        self.solution = 11 * self.random_int

    def print_problem(self):
        self.generate_problem()
        self.get_user_input(f"11 * {self.random_int}\n")
        self.check_solution()


    def print_instructions(self):
        instructions = "Multiply an integer of 2 digits or more by 11 is quite easy, let's make some examples: "\
        "\nexample 1: 11 * 12 = 132 -> the leftmost digit of the result (1) is the leftmost digit of the integer, "\
        "\nwhile the rightmost digit of the result (2) is the rightmost digit of the integer. "\
        "\nThe middle digit (3) is the sum of the leftmost and rightmost digits of the integer (1+2)"\
        "\n"\
        "\nexample 2: 11 * 75 = 825 -> you can follow the same rule as before, but now the middle digit is 7 + 5 = 12. "\
        "\nTo obtain the result, you simply have to add the number in the decimal place of 12 (1) to the leftmost digit. "\
        "\nSo we obtain (7+1) (7+5 - 10) (5) -> 825. "\
        "\n"\
        "\nWith three digits the process is quite similar: "\
        "\n11 * 123 = 1353 -> leftmost is 1, rightmost is 3, the middle digits are 1+2 and 2+3."\
        "\n"

        print_instructions = input("Do you want to read the instructions? (y/n)")
        if print_instructions == 'y':
            print(instructions)

    @staticmethod
    def return_exercise_type():
        return "Multiplication by 11"