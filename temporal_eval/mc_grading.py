
class MC_Grading:
    def __init__(self):
        self.results = []

    def grade_mcq(self, input, expected, allowed_labels=("A","B")):
        lines = input.strip().splitlines()
        first_line = lines[0] if lines else ""
        choice = first_line.partition(".")[0].strip().upper()

        valid = choice in allowed_labels
        return valid and choice == expected.strip().upper()