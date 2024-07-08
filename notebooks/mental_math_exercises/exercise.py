import mult_by_eleven, \
multiply_two_digits_number_ending_in_five, \
multiply_two_digits_number_with_last_digits_sum_to_ten

exercise_menu = {
    1: mult_by_eleven.Mult_by_eleven,
    2: multiply_two_digits_number_ending_in_five.Multiply_two_digits_number_ending_in_five,
    3: multiply_two_digits_number_with_last_digits_sum_to_ten.Multiply_two_digits_number_with_last_digits_sum_to_ten,

}

print("What exercise do you want to do?\n")

for key, value in exercise_menu.items():
    print(f"{key} -> {value.return_exercise_type()}")

ex = int(input("\nInput the exercise you want to do: \n"))

print("")

s = exercise_menu[ex]()
s.start_exercise()