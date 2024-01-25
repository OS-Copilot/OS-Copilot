from jarvis.action.base_action import BaseAction

class calculate_ISBN10_digits(BaseAction):
    def __init__(self):
        self._description = "Calculate the ISBN-10 check digits for the provided 9-digit numbers."

    def __call__(self, numbers, *args, **kwargs):
        """
        Calculate the ISBN-10 check digits for the provided 9-digit numbers and replace any 'X' with '0'.

        Args:
            numbers (list of str): The list of 9-digit numbers as strings for which the check digits are to be calculated.

        Returns:
            list of str: The list of calculated check digits for the provided numbers.
        """
        check_digits = []
        for number in numbers:
            try:
                # Replace 'X' with '0' and calculate the check digit
                number = number.replace('X', '0')
                total = sum((i + 1) * int(digit) for i, digit in enumerate(number))
                check_digit = total % 11
                check_digit = 'X' if check_digit == 10 else str(check_digit)
                check_digits.append(check_digit)
                print(f"Check digit for ISBN-10 number {number} is {check_digit}.")
            except ValueError as e:
                print(f"Invalid number {number}: {e}")
            except Exception as e:
                print(f"An error occurred while calculating the check digit for {number}: {e}")
        return check_digits

# Example of how to use the class (this should be in the comments):
# check_digit_calculator = calculate_ISBN10_digits()
# check_digits = check_digit_calculator(numbers=["478225952", "643485613", "739394228", "291726859", "875262394", "542617795", "031810713", "957007669", "871467426"])