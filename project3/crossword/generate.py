import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains.keys():
            for word in self.domains[var].copy():
                if var.length != len(word):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False
        i, j = self.crossword.overlaps[x, y]
        for x_word in self.domains[x].copy():
            found = False
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    found = True
            if not found:
                self.domains[x].remove(x_word)
        return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        all_arcs = False
        if arcs is None:
            arcs = []
            all_arcs = True
            for x in self.domains:
                for y in self.domains:
                    if x == y:
                        continue
                    arcs.append((x, y))
        while len(arcs) > 0:
            x, y = arcs[0]
            arcs = arcs[1:]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                if not all_arcs:
                    continue
                for neighbor in self.crossword.neighbors(x):
                    if neighbor == y:
                        continue
                    arcs.append((neighbor, x))
        return True        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(self.crossword.variables) == len(assignment)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(set(assignment.values())) != len(assignment.values()):
            return False
        for var in assignment.keys():
            if var.length != len(assignment[var]):
                return False
        for x in assignment.keys():
            for y in assignment.keys():
                if x == y:
                    continue
                if self.crossword.overlaps[x, y] is None:
                    continue
                i, j = self.crossword.overlaps[x, y]
                if assignment[x][i] != assignment[y][j]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = {}
        for solution in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = solution
            if not self.consistent(new_assignment):
                continue
            eliminations = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment.keys():
                    continue
                i, j = self.crossword.overlaps[var, neighbor]
                eliminations += len([x for x in self.domains[neighbor] if solution[i] != x[j]])
            values[solution] = eliminations
        sorted_values = [k for k, v in sorted(values.items(), key=lambda item: item[1])]
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining_values = {var: len(self.domains[var])
                            for var in self.domains.keys() - assignment.keys()}
        sorted_remaining_values = [(k, v) for k, v in sorted(
            remaining_values.items(), key=lambda item: item[1])]
        ties = [(k, v) for k, v in sorted_remaining_values if v == sorted_remaining_values[0][1]]
        if len(ties) == 1:
            return ties[0][0]
        sorted_ties = [k for k, v in sorted(
            ties, reverse=True, key=lambda var: len(self.crossword.neighbors(var[0])))]
        return sorted_ties[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        next = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(next, assignment):
            new_assignment = assignment.copy()
            new_assignment[next] = value
            new_assignment = self.backtrack(new_assignment)
            if new_assignment is not None:
                return new_assignment
        return None
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
