import numpy as np
from abc import ABC, abstractmethod


class Problem(ABC):

    def __init__(self):
        return
    
    def get_user_input(self, message):
        self.user_input = int(input(message))

    def check_solution(self):
        if self.user_input == self.solution:
            print("Correct!\n")
        else:
            print(f"The correct solution was {self.solution}.\n")

    def start_exercise(self):
        self.print_instructions()
        while True:
            self.print_problem()

    @abstractmethod
    def print_problem(self):
        pass

    @abstractmethod
    def print_instructions(self):
        pass

    @abstractmethod
    def generate_problem(self):
        pass

    @abstractmethod
    def return_exercise_type():
        pass